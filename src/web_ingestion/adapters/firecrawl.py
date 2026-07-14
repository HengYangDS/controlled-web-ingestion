"""Loopback-only Firecrawl protocol adapter."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class FirecrawlResult:
    content: str
    title: str | None
    final_url: str
    discovered_count: int


class FirecrawlClient:
    """Talk only to an explicitly supplied local Firecrawl API endpoint."""

    def __init__(self, endpoint: str, *, timeout_seconds: float = 45.0) -> None:
        parsed = urlsplit(endpoint)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "::1", "localhost"}:
            raise ValueError("Firecrawl endpoint must be loopback HTTP")
        self.endpoint = endpoint.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None, *, timeout_seconds: float | None = None) -> dict[str, Any]:
        encoded = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(f"{self.endpoint}{path}", data=encoded, method=method, headers={"Content-Type": "application/json"} if encoded else {})
        with urlopen(request, timeout=self.timeout_seconds if timeout_seconds is None else timeout_seconds) as response:  # noqa: S310 - loopback validated
            data = json.loads(response.read().decode("utf-8"))
        if not isinstance(data, dict) or data.get("success") is False:
            raise RuntimeError(f"Firecrawl API {method} {path} returned unsuccessful payload")
        return data

    @staticmethod
    def _result_from_page(page: dict[str, Any], *, discovered_count: int) -> FirecrawlResult:
        metadata = page.get("metadata") if isinstance(page.get("metadata"), dict) else {}
        content = page.get("markdown") or page.get("content") or ""
        title = metadata.get("title") if isinstance(metadata.get("title"), str) else None
        final_url = metadata.get("sourceURL") or metadata.get("url") or page.get("url")
        if not isinstance(final_url, str) or not final_url:
            raise RuntimeError("Firecrawl response omitted source URL")
        return FirecrawlResult(str(content), title, final_url, discovered_count)

    def scrape(self, url: str) -> FirecrawlResult:
        response = self._request("POST", "/v1/scrape", {"url": url, "formats": ["markdown"]})
        page = response.get("data")
        if not isinstance(page, dict):
            raise RuntimeError("Firecrawl scrape response omitted page data")
        return self._result_from_page(page, discovered_count=1)

    def crawl(self, url: str, *, max_pages: int, poll_interval_seconds: float = 0.1) -> FirecrawlResult:
        deadline = time.monotonic() + self.timeout_seconds
        crawl_id: str | None = None
        try:
            created = self._request("POST", "/v1/crawl", {"url": url, "limit": max_pages, "maxConcurrency": 1, "maxDiscoveryDepth": 1, "allowBackwardLinks": False, "ignoreSitemap": True, "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True, "timeout": 10_000}}, timeout_seconds=max(0.001, deadline - time.monotonic()))
            crawl_id = created.get("id")
            if not isinstance(crawl_id, str) or not crawl_id:
                raise RuntimeError("Firecrawl crawl response omitted job identifier")
            while time.monotonic() < deadline:
                status = self._request("GET", f"/v1/crawl/{crawl_id}", timeout_seconds=max(0.001, deadline - time.monotonic()))
                if status.get("status") == "completed":
                    data = status.get("data")
                    pages = [item for item in data if isinstance(item, dict)][:max_pages] if isinstance(data, list) else []
                    if not pages:
                        raise RuntimeError("Firecrawl completed crawl without valid pages")
                    return self._result_from_page(pages[0], discovered_count=len(pages))
                if status.get("status") in {"failed", "cancelled"}:
                    raise RuntimeError(f"Firecrawl crawl ended with status {status.get('status')}")
                time.sleep(min(poll_interval_seconds, max(0.0, deadline - time.monotonic())))
        except (TimeoutError, OSError):
            if crawl_id:
                self._best_effort_cancel(crawl_id)
            raise TimeoutError(f"Firecrawl crawl {crawl_id or 'unknown'} exceeded {self.timeout_seconds} seconds")
        if crawl_id:
            self._best_effort_cancel(crawl_id)
        raise TimeoutError(f"Firecrawl crawl {crawl_id or 'unknown'} exceeded {self.timeout_seconds} seconds")

    def _best_effort_cancel(self, crawl_id: str) -> None:
        try:
            self._request("DELETE", f"/v1/crawl/{crawl_id}", timeout_seconds=min(5.0, self.timeout_seconds))
        except (OSError, RuntimeError, ValueError):
            return

    def cancel(self, crawl_id: str) -> None:
        self._request("DELETE", f"/v1/crawl/{crawl_id}")
