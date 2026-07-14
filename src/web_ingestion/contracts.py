"""Stable runtime contracts for Controlled Web Ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

MODES = frozenset({"static", "browser", "crawl"})
MAX_PAGES = 10
MODE_PAGE_LIMITS = {"static": 1, "browser": 1, "crawl": MAX_PAGES}
MAX_TIMEOUT_SECONDS = 120.0
MAX_RESPONSE_BYTES = 4 * 1024 * 1024


class IngestionError(ValueError):
    """A request was unsafe, out of policy, or unable to yield a receipt."""


@dataclass(frozen=True)
class IngestionRequest:
    url: str
    purpose: str
    mode: str
    max_pages: int
    timeout_seconds: float
    engine: str | None = None

    def __post_init__(self) -> None:
        if not self.purpose.strip():
            raise IngestionError("purpose is required")
        if self.mode not in MODES:
            raise IngestionError(f"mode must be one of {sorted(MODES)}")
        if not 1 <= self.max_pages <= MAX_PAGES:
            raise IngestionError(f"max_pages must be between 1 and {MAX_PAGES}")
        if self.max_pages > MODE_PAGE_LIMITS[self.mode]:
            raise IngestionError(f"max_pages_for_mode:{self.mode}={MODE_PAGE_LIMITS[self.mode]}")
        if not 0 < self.timeout_seconds <= MAX_TIMEOUT_SECONDS:
            raise IngestionError(f"timeout must be between 0 and {MAX_TIMEOUT_SECONDS:g} seconds")


@dataclass(frozen=True)
class RawHttpResponse:
    url: str
    status_code: int
    headers: dict[str, str]
    body: bytes


@dataclass(frozen=True)
class HttpFetch:
    requested_url: str
    final_url: str
    status_code: int
    headers: dict[str, str]
    body: bytes
    redirect_chain: tuple[str, ...]


@dataclass(frozen=True)
class IngestionOutcome:
    request_id: str
    route: str
    stage_receipt: Path
    content: str
