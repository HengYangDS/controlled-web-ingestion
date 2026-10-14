"""In-memory static extraction adapter."""

from __future__ import annotations

from ..contracts import IngestionError


def extract(content: bytes) -> str:
    import trafilatura

    extracted = trafilatura.extract(
        content.decode("utf-8", errors="replace"), include_comments=False
    )
    if not extracted:
        raise IngestionError("static_extraction_empty")
    return extracted
