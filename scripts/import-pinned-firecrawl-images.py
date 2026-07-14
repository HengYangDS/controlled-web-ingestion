#!/usr/bin/env python3
"""Import fixed official Firecrawl GHCR images without a registry mirror.

This is a recovery path for a host where long GHCR CDN streams are truncated.
Each object is range-fetched only from its official signed GHCR URL, verified
against the exact official platform manifest digest, then loaded locally. No
Docker daemon configuration is changed.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ghcr_registry import GhcrRegistry

DEFAULT_SPEC = ROOT / "ops" / "firecrawl-images.json"


def import_images(*, spec_path: Path, cache_dir: Path, workers: int, chunk_bytes: int, timeout_seconds: float) -> list[str]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if spec.get("platform_manifest") != "linux/arm64":
        raise ValueError("only the reviewed linux/arm64 manifests are admissible on this host")
    imported: list[str] = []
    for item in spec.get("images", []):
        repository = item["repository"]
        tag = item["tag"]
        manifest_digest = item["manifest_digest"]
        image_cache = cache_dir / item["name"]
        archive = image_cache / "image.tar"
        registry = GhcrRegistry(repository, timeout_seconds=timeout_seconds)
        registry.export_docker_archive(
            tag=tag,
            platform_manifest_digest=manifest_digest,
            output=archive,
            cache_dir=image_cache / "blobs",
            chunk_bytes=chunk_bytes,
            workers=workers,
        )
        subprocess.run(["docker", "load", "--input", str(archive)], check=True)
        image = f"ghcr.io/{repository}:{tag}"
        subprocess.run(["docker", "image", "inspect", image], check=True, stdout=subprocess.DEVNULL)
        imported.append(image)
    return imported


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--chunk-bytes", type=int, default=1 << 20)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    args = parser.parse_args()
    if args.cache_dir is None:
        args.cache_dir = Path(tempfile.mkdtemp(prefix="firecrawl-ghcr-import-"))
        ephemeral = True
    else:
        ephemeral = False
    try:
        for image in import_images(spec_path=args.spec, cache_dir=args.cache_dir, workers=args.workers, chunk_bytes=args.chunk_bytes, timeout_seconds=args.timeout_seconds):
            print(image)
    finally:
        if ephemeral:
            shutil.rmtree(args.cache_dir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
