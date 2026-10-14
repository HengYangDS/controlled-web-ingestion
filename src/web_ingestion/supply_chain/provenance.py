"""Verify the local Firecrawl topology images against reviewed provenance."""

from __future__ import annotations

from typing import Any

SCHEMA = "firecrawl-isolated-image-provenance-v2"


def _repository(name: str) -> str:
    """Return a repository name without Docker Hub's implicit registry and namespace."""
    for prefix in ("docker.io/library/", "docker.io/"):
        if name.startswith(prefix):
            return name.removeprefix(prefix)
    return name


def pinned_reference(entry: dict[str, Any]) -> str:
    """Return the digest reference that Compose and the verifier both use for one image."""
    repository = str(entry["reference"]).rsplit(":", 1)[0]
    return f"{repository}@{entry['manifest_digest']}"


def verify_image_records(provenance: dict[str, Any], images: list[dict[str, Any]]) -> list[str]:
    """Return deterministic errors for digest, platform, or local-ID drift."""
    if provenance.get("schema") != SCHEMA:
        return [f"provenance schema must be {SCHEMA}"]
    if provenance.get("platform") != "linux/arm64":
        return ["platform must be linux/arm64"]
    provenance_images = provenance.get("images")
    if not isinstance(provenance_images, dict):
        return ["provenance images must be an object"]
    by_digest: dict[tuple[str, str], dict[str, Any]] = {}
    for image in images:
        for repo_digest in image.get("RepoDigests", []) if isinstance(image, dict) else ():
            repository, separator, digest = str(repo_digest).partition("@")
            if separator:
                by_digest[(_repository(repository), digest)] = image
    errors: list[str] = []
    for name, expected in sorted(provenance_images.items()):
        if not isinstance(expected, dict) or not all(
            isinstance(expected.get(key), str)
            for key in ("reference", "manifest_digest", "local_image_id")
        ):
            errors.append(f"{name}: reference, manifest_digest and local_image_id are required")
            continue
        repository, _, digest = pinned_reference(expected).partition("@")
        actual = by_digest.get((_repository(repository), digest))
        if actual is None:
            errors.append(f"{name}: missing image {pinned_reference(expected)}")
            continue
        if actual.get("Os") != "linux" or actual.get("Architecture") != "arm64":
            errors.append(f"{name}: architecture must be linux/arm64")
        if actual.get("Id") != expected["local_image_id"]:
            errors.append(f"{name}: image_id does not match reviewed local image identity")
    return errors
