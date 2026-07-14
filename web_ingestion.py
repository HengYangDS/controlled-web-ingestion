"""Controlled, body-redacted on-demand Web-Ingestion controller.

This module is deliberately an admission and receipt layer. It does not
register tools, start persistent services, or write into any RAG system.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import urljoin, urlsplit

from admission import (
    StageStore,
    TargetPolicy,
    canonicalize_url,
    evaluate_robots,
    is_allowed_content_type,
    validate_target,
)


USER_AGENT = "AgenticWebIngestion/1.0 (+local, contact: disabled)"
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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_transport(url: str, *, timeout_seconds: float, max_bytes: int) -> RawHttpResponse:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
            return None

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    opener = urllib.request.build_opener(NoRedirect)
    try:
        response = opener.open(request, timeout=timeout_seconds)  # noqa: S310 - admission validates target first
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        headers = {key: value for key, value in response.headers.items()}
        return RawHttpResponse(
            url=response.geturl(),
            status_code=response.status,
            headers=headers,
            body=response.read(max_bytes + 1),
        )


class SafeHttpClient:
    """Fetch public HTTP(S) targets one hop at a time after policy admission."""

    def __init__(
        self,
        *,
        resolver: Callable[[str], Iterable[str]] | None = None,
        transport: Callable[..., RawHttpResponse] = _default_transport,
    ) -> None:
        self.resolver = resolver
        self.transport = transport

    def _admit(self, url: str) -> str:
        kwargs = {"policy": TargetPolicy()}
        if self.resolver is not None:
            kwargs["resolver"] = self.resolver
        decision = validate_target(url, **kwargs)
        if not decision.allowed:
            raise IngestionError(decision.reason)
        return decision.canonical_url

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> HttpFetch:
        started = time.monotonic()
        current = self._admit(url)
        chain = [current]
        for _ in range(6):
            remaining = timeout_seconds - (time.monotonic() - started)
            if remaining <= 0:
                raise IngestionError("request_timeout")
            response = self.transport(current, timeout_seconds=remaining, max_bytes=max_bytes)
            if len(response.body) > max_bytes:
                raise IngestionError("response_exceeds_byte_budget")
            if response.status_code in {301, 302, 303, 307, 308}:
                location = response.headers.get("Location")
                if not location:
                    raise IngestionError("redirect_without_location")
                current = self._admit(urljoin(current, location))
                chain.append(current)
                continue
            if response.status_code >= 400:
                raise IngestionError(f"http_status:{response.status_code}")
            return HttpFetch(
                requested_url=chain[0],
                final_url=current,
                status_code=response.status_code,
                headers=response.headers,
                body=response.body,
                redirect_chain=tuple(chain),
            )
        raise IngestionError("redirect_limit_exceeded")

    def fetch_robots(self, url: str, *, timeout_seconds: float):
        parts = urlsplit(url)
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        try:
            response = self.fetch(robots_url, timeout_seconds=timeout_seconds, max_bytes=256 * 1024)
        except IngestionError as exc:
            if str(exc) == "http_status:404":
                return evaluate_robots("", url)
            raise IngestionError(f"robots_unavailable:{exc}") from exc
        return evaluate_robots(response.body.decode("utf-8", errors="replace"), url, user_agent=USER_AGENT)


def _default_static_extractor(content: bytes) -> str:
    import trafilatura

    extracted = trafilatura.extract(content.decode("utf-8", errors="replace"), include_comments=False)
    if not extracted:
        raise IngestionError("static_extraction_empty")
    return extracted


class IngestionController:
    """Route a validated request, then stage a redacted receipt and nothing else."""

    def __init__(
        self,
        *,
        http_client: SafeHttpClient | object | None = None,
        static_extractor: Callable[[bytes], str] = _default_static_extractor,
        browser_handler: Callable[[IngestionRequest], tuple[str, str | None, str, int]] | None = None,
    ) -> None:
        self.http_client = http_client or SafeHttpClient()
        self.static_extractor = static_extractor
        self.browser_handler = browser_handler

    @staticmethod
    def _request_id(request: IngestionRequest) -> str:
        payload = "\0".join((request.url, request.purpose, request.mode, str(request.max_pages)))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]

    @staticmethod
    def _has_duplicate(stage_root: Path, digest: str) -> bool:
        staging = stage_root / "staging"
        if not staging.exists():
            return False
        for path in staging.glob("*.json"):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if record.get("content_sha256") == digest:
                return True
        return False

    def _stage(
        self,
        *,
        request: IngestionRequest,
        stage_root: Path,
        route: str,
        content: str,
        title: str | None,
        fetch: HttpFetch,
        robots_decision: str,
        discovered_count: int,
        content_type: str,
    ) -> IngestionOutcome:
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        duplicate = self._has_duplicate(stage_root, digest)
        status = "duplicate" if duplicate else "success"
        record = {
            "candidate": route,
            "request_id": self._request_id(request),
            "purpose": request.purpose.strip(),
            "route": route,
            "requested_url": fetch.requested_url,
            "final_url": fetch.final_url,
            "source_url": fetch.final_url,
            "content_sha256": digest,
            "status": status,
            "content_type": content_type,
            "fetched_at": utc_now(),
            "parser_version": f"{route}@m2",
            "robots_decision": robots_decision,
            "policy_decision": "admitted",
            "redirect_chain": list(fetch.redirect_chain),
            "dedupe_decision": "duplicate" if duplicate else "unique",
            "budget": {"max_pages": request.max_pages, "timeout_seconds": request.timeout_seconds},
            "quality": {"characters": len(content), "title_present": bool(title), "discovered_count": discovered_count},
        }
        receipt = StageStore(stage_root).stage(record)
        return IngestionOutcome(record["request_id"], route, receipt, content)

    def ingest(self, request: IngestionRequest, *, stage_root: Path) -> IngestionOutcome:
        target, robots = self.preflight(request)
        if request.mode == "static":
            content = self.static_extractor(target.body)
            return self._stage(
                request=request,
                stage_root=stage_root,
                route="trafilatura",
                content=content,
                title=None,
                fetch=target,
                robots_decision="allowed",
                discovered_count=1,
                content_type=target.headers["Content-Type"],
            )
        if self.browser_handler is None:
            raise IngestionError("browser_route_requires_controlled_firecrawl_handler")
        browser_request = IngestionRequest(
            url=target.final_url,
            purpose=request.purpose,
            mode=request.mode,
            max_pages=request.max_pages,
            timeout_seconds=request.timeout_seconds,
            engine=request.engine,
        )
        content, title, final_url, discovered_count = self.browser_handler(browser_request)
        if not 1 <= discovered_count <= request.max_pages:
            raise IngestionError("discovered_count_exceeds_page_budget")
        # The isolated service is deliberately not trusted as an egress-policy
        # oracle. Its reported source URL must still be a public HTTP(S) target
        # before it can enter a receipt; otherwise a compromised or regressed
        # service could smuggle a private final target into the data plane.
        result_target = validate_target(final_url, policy=TargetPolicy())
        if not result_target.allowed:
            raise IngestionError(f"firecrawl_result_target:{result_target.reason}")
        fetch = HttpFetch(
            requested_url=target.requested_url,
            final_url=result_target.canonical_url,
            status_code=200,
            headers=target.headers,
            body=b"",
            redirect_chain=target.redirect_chain,
        )
        return self._stage(
            request=request,
            stage_root=stage_root,
            route="firecrawl",
            content=content,
            title=title,
            fetch=fetch,
            robots_decision="allowed",
            discovered_count=discovered_count,
            content_type=target.headers["Content-Type"],
        )

    def preflight(self, request: IngestionRequest) -> tuple[HttpFetch, object]:
        """Perform public-target, redirect, robots, and MIME admission before any route starts."""
        target = self.http_client.fetch(request.url, timeout_seconds=request.timeout_seconds, max_bytes=MAX_RESPONSE_BYTES)
        robots = self.http_client.fetch_robots(target.final_url, timeout_seconds=min(15.0, request.timeout_seconds))
        if not robots.allowed:
            raise IngestionError(robots.reason)
        if not is_allowed_content_type(target.headers.get("Content-Type")):
            raise IngestionError("content_type_not_allowed")
        return target, robots
