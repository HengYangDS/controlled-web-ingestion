"""Create a `docker load` archive only from digest-verified GHCR objects."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
from pathlib import Path


class ImageArchiveError(RuntimeError):
    """An image config or compressed layer does not match the manifest."""


def _digest(payload: bytes) -> str:
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _safe_digest_name(digest: str) -> str:
    if not digest.startswith("sha256:") or len(digest) != 71:
        raise ImageArchiveError(f"invalid digest {digest!r}")
    return digest.split(":", 1)[1]


def build_docker_archive(
    *,
    config_bytes: bytes,
    config_digest: str,
    layer_blobs: list[tuple[str, Path]],
    repository: str,
    tag: str,
    output: Path,
) -> Path:
    """Convert verified OCI gzip layers into a Docker-compatible load archive."""
    if _digest(config_bytes) != config_digest:
        raise ImageArchiveError("config digest does not match manifest")
    work = Path(tempfile.mkdtemp(prefix="docker-archive-", dir=output.parent))
    try:
        config_name = f"{_safe_digest_name(config_digest)}.json"
        (work / config_name).write_bytes(config_bytes)
        layer_names: list[str] = []
        for index, (expected_digest, compressed_path) in enumerate(layer_blobs):
            compressed = compressed_path.read_bytes()
            if _digest(compressed) != expected_digest:
                raise ImageArchiveError(f"layer {index} digest does not match manifest")
            try:
                layer_tar = gzip.decompress(compressed)
                with tarfile.open(fileobj=io.BytesIO(layer_tar), mode="r:"):
                    pass
            except (OSError, tarfile.TarError) as exc:
                raise ImageArchiveError(f"layer {index} is not a valid gzip tar payload") from exc
            layer_dir = work / f"layer-{index:03d}"
            layer_dir.mkdir()
            (layer_dir / "layer.tar").write_bytes(layer_tar)
            (layer_dir / "VERSION").write_text("1.0\n", encoding="utf-8")
            (layer_dir / "json").write_text("{}\n", encoding="utf-8")
            layer_names.append(f"{layer_dir.name}/layer.tar")
        manifest = [
            {"Config": config_name, "RepoTags": [f"{repository}:{tag}"], "Layers": layer_names}
        ]
        (work / "manifest.json").write_text(
            json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8"
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(output.suffix + ".tmp")
        with tarfile.open(temporary, mode="w") as archive:
            for child in sorted(work.iterdir(), key=lambda path: path.name):
                archive.add(child, arcname=child.name, recursive=True)
        temporary.replace(output)
        return output
    except BaseException:
        output.unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(work, ignore_errors=True)
