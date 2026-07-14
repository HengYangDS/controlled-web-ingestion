"""Minimal authenticated GHCR Registry v2 reader for fixed image digests."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

from ghcr_image_archive import build_docker_archive
from ghcr_range import fetch_blob_by_ranges


class RegistryError(RuntimeError):
    """A registry response was malformed or did not meet pinned-image rules."""


MANIFEST_ACCEPT = (
    "application/vnd.docker.distribution.manifest.list.v2+json, "
    "application/vnd.oci.image.index.v1+json, "
    "application/vnd.docker.distribution.manifest.v2+json"
)


def select_platform_manifest(index: dict[str, Any], *, architecture: str, os_name: str = "linux") -> str:
    for descriptor in index.get("manifests", []):
        platform = descriptor.get("platform") if isinstance(descriptor, dict) else None
        if isinstance(platform, dict) and platform.get("os") == os_name and platform.get("architecture") == architecture:
            digest = descriptor.get("digest")
            if isinstance(digest, str):
                return digest
    raise RegistryError(f"image index has no {os_name}/{architecture} manifest")


def manifest_blobs(manifest: dict[str, Any]) -> tuple[tuple[str, int], list[tuple[str, int]]]:
    config = manifest.get("config")
    layers = manifest.get("layers")
    if not isinstance(config, dict) or not isinstance(layers, list):
        raise RegistryError("expected a single-platform Docker manifest")

    def descriptor(value: Any) -> tuple[str, int]:
        if not isinstance(value, dict) or not isinstance(value.get("digest"), str) or not isinstance(value.get("size"), int):
            raise RegistryError("manifest blob descriptor is invalid")
        return value["digest"], value["size"]

    return descriptor(config), [descriptor(layer) for layer in layers]


class GhcrRegistry:
    """Fetch only declared official GHCR objects; no mirror or daemon mutation."""

    def __init__(self, repository: str, *, timeout_seconds: float = 60.0) -> None:
        self.repository = repository
        self.timeout_seconds = timeout_seconds
        self.token = self._token()

    def _open(self, url: str, *, headers: dict[str, str] | None = None) -> bytes:
        merged = {"Authorization": f"Bearer {self.token}"}
        if headers:
            merged.update(headers)
        request = Request(url, headers=merged)
        with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310 - GHCR URLs are constructed below
            return response.read()

    def _token(self) -> str:
        query = urlencode({"service": "ghcr.io", "scope": f"repository:{self.repository}:pull"})
        request = Request(f"https://ghcr.io/token?{query}")
        with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310 - constant GHCR origin
            payload = json.loads(response.read().decode("utf-8"))
        token = payload.get("token")
        if not isinstance(token, str) or not token:
            raise RegistryError("GHCR did not issue a pull token")
        return token

    def manifest(self, reference: str) -> dict[str, Any]:
        raw = self._open(
            f"https://ghcr.io/v2/{self.repository}/manifests/{reference}",
            headers={"Accept": MANIFEST_ACCEPT},
        )
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise RegistryError("GHCR manifest is not an object")
        return data

    def verify_tag_platform_digest(self, *, tag: str, platform_digest: str, architecture: str = "arm64") -> None:
        """Bind a human-readable release tag to its reviewed platform digest."""
        resolved = select_platform_manifest(self.manifest(tag), architecture=architecture)
        if resolved != platform_digest:
            raise RegistryError(
                f"tag {tag!r} resolved to {resolved}, not reviewed digest {platform_digest}"
            )

    def signed_blob_url(self, digest: str) -> str:
        # Do not follow the redirect: a plain GET is intentionally avoided because
        # this workstation truncates long continuous CDN streams. Range requests
        # below will use the signed URL directly.
        class NoRedirect(HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
                return None

        request = Request(f"https://ghcr.io/v2/{self.repository}/blobs/{digest}", headers={"Authorization": f"Bearer {self.token}"})
        try:
            response = build_opener(NoRedirect).open(request, timeout=self.timeout_seconds)  # noqa: S310 - trusted registry origin
        except HTTPError as exc:
            if exc.code not in {301, 302, 303, 307, 308}:
                raise
            location = exc.headers.get("Location")
        else:
            location = response.headers.get("Location")
        if not isinstance(location, str) or not location.startswith("https://pkg-containers.githubusercontent.com/"):
            raise RegistryError("GHCR did not issue an expected signed package URL")
        return location

    def blob_bytes(self, digest: str) -> bytes:
        return self._open(f"https://ghcr.io/v2/{self.repository}/blobs/{digest}")

    def blob_to_path(self, *, digest: str, size: int, destination: Path, chunk_bytes: int = 1 << 20, workers: int = 4) -> Path:
        def get_range(start: int, end: int) -> bytes:
            # GHCR package URLs are signed and short-lived. Refreshing for every
            # chunk makes a resumable import survive expiration during large
            # images, without contacting any mirror.
            url = self.signed_blob_url(digest)
            response = subprocess.run(
                [
                    "curl",
                    "--silent",
                    "--show-error",
                    "--fail",
                    "--ipv4",
                    "--connect-timeout",
                    "10",
                    "--max-time",
                    str(int(self.timeout_seconds)),
                    "--range",
                    f"{start}-{end}",
                    url,
                ],
                check=True,
                capture_output=True,
            )
            return response.stdout

        return fetch_blob_by_ranges(
            total_bytes=size,
            expected_sha256=digest.removeprefix("sha256:"),
            destination=destination,
            fetch_range=get_range,
            chunk_bytes=chunk_bytes,
            workers=workers,
        )

    def export_docker_archive(
        self,
        *,
        tag: str,
        platform_manifest_digest: str,
        output: Path,
        cache_dir: Path,
        chunk_bytes: int = 1 << 20,
        workers: int = 4,
    ) -> Path:
        self.verify_tag_platform_digest(tag=tag, platform_digest=platform_manifest_digest)
        manifest = self.manifest(platform_manifest_digest)
        (config_digest, _config_size), layers = manifest_blobs(manifest)
        config = self.blob_bytes(config_digest)
        layer_paths: list[tuple[str, Path]] = []
        cache_dir.mkdir(parents=True, exist_ok=True)
        for digest, size in layers:
            path = cache_dir / f"{digest.removeprefix('sha256:')}.gz"
            self.blob_to_path(digest=digest, size=size, destination=path, chunk_bytes=chunk_bytes, workers=workers)
            layer_paths.append((digest, path))
        return build_docker_archive(
            config_bytes=config,
            config_digest=config_digest,
            layer_blobs=layer_paths,
            repository=f"ghcr.io/{self.repository}",
            tag=tag,
            output=output,
        )
