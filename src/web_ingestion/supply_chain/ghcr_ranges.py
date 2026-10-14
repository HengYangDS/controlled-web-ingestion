"""Verified range-based GHCR blob retrieval for a network that truncates streams.

This is a narrowly-scoped recovery transport. It accepts only a digest supplied
by an already-verified official manifest and refuses to publish a partial or
digest-mismatched blob.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import time
from collections.abc import Callable
from pathlib import Path


class BlobIntegrityError(RuntimeError):
    """An assembled blob was incomplete or did not match its expected digest."""


def byte_ranges(*, total_bytes: int, chunk_bytes: int) -> list[tuple[int, int]]:
    if total_bytes < 0 or chunk_bytes <= 0:
        raise ValueError("total_bytes must be non-negative and chunk_bytes positive")
    return [
        (start, min(total_bytes - 1, start + chunk_bytes - 1))
        for start in range(0, total_bytes, chunk_bytes)
    ]


def fetch_blob_by_ranges(
    *,
    total_bytes: int,
    expected_sha256: str,
    destination: Path,
    fetch_range: Callable[[int, int], bytes],
    chunk_bytes: int = 1 << 20,
    workers: int = 4,
    max_retries: int = 4,
) -> Path:
    """Fetch each precise byte range, then atomically publish only verified data."""
    if len(expected_sha256) != 64 or any(
        char not in "0123456789abcdef" for char in expected_sha256
    ):
        raise ValueError("expected_sha256 must be a lowercase SHA-256 hex digest")
    if workers < 1 or max_retries < 1:
        raise ValueError("workers and max_retries must be positive")
    destination.parent.mkdir(parents=True, exist_ok=True)
    work = destination.parent / f".{destination.name}.parts"
    work.mkdir(parents=True, exist_ok=True)

    def one(index: int, start: int, end: int) -> tuple[int, Path]:
        expected_length = end - start + 1
        path = work / f"{index:08d}.part"
        if path.is_file() and path.stat().st_size == expected_length:
            return index, path
        path.unlink(missing_ok=True)
        last_error: BaseException | None = None
        for attempt in range(max_retries):
            try:
                payload = fetch_range(start, end)
                if len(payload) != expected_length:
                    raise BlobIntegrityError(
                        f"range {start}-{end} returned {len(payload)} bytes, "
                        f"expected {expected_length}"
                    )
                path.write_bytes(payload)
                return index, path
            except BaseException as exc:  # network callable can expose any transport exception
                last_error = exc
                if attempt + 1 < max_retries:
                    time.sleep(0.1 * (attempt + 1))
        raise BlobIntegrityError(
            f"range {start}-{end} did not complete after {max_retries} attempts: {last_error}"
        )

    try:
        ranges = byte_ranges(total_bytes=total_bytes, chunk_bytes=chunk_bytes)
        completed: dict[int, Path] = {}
        # Keep requests serialized. The observed path accepts byte ranges but
        # becomes markedly less reliable under concurrent long-lived HTTPS
        # connections. ``workers`` is retained in the public signature for
        # caller compatibility, but intentionally does not widen transport.
        for index, (start, end) in enumerate(ranges):
            completed_index, path = one(index, start, end)
            completed[completed_index] = path
        temporary = work / "assembled.tmp"
        with temporary.open("wb") as output:
            for index in range(len(ranges)):
                with completed[index].open("rb") as part:
                    shutil.copyfileobj(part, output)
        if temporary.stat().st_size != total_bytes:
            raise BlobIntegrityError(
                f"assembled blob has {temporary.stat().st_size} bytes, expected {total_bytes}"
            )
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        if digest != expected_sha256:
            raise BlobIntegrityError(f"assembled blob digest mismatch: {digest}")
        published = destination.with_suffix(destination.suffix + ".tmp")
        os.replace(temporary, published)
        os.replace(published, destination)
        shutil.rmtree(work, ignore_errors=True)
        return destination
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
