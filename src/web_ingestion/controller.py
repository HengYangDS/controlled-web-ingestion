"""Request lifecycle and adapter routing for Controlled Web Ingestion."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path

from .adapters.static import extract as default_static_extractor
from .contracts import (
    MAX_RESPONSE_BYTES,
    HttpFetch,
    IngestionError,
    IngestionOutcome,
    IngestionRequest,
)
from .policy import TargetPolicy, is_allowed_content_type, validate_target
from .staging import StageStore, utc_now
from .transport import SafeHttpClient


class IngestionController:
    """Route a validated request, then stage a redacted receipt and nothing else."""

    def __init__(
        self,
        *,
        http_client: SafeHttpClient | object | None = None,
        static_extractor: Callable[[bytes], str] = default_static_extractor,
        browser_handler: Callable[[IngestionRequest], tuple[str, str | None, str, int]]
        | None = None,
    ) -> None:
        self.http_client = http_client or SafeHttpClient()
        self.static_extractor = static_extractor
        self.browser_handler = browser_handler

    @staticmethod
    def _request_id(request: IngestionRequest) -> str:
        return hashlib.sha256(
            "\0".join((request.url, request.purpose, request.mode, str(request.max_pages))).encode(
                "utf-8"
            )
        ).hexdigest()[:24]

    @staticmethod
    def _has_duplicate(stage_root: Path, digest: str) -> bool:
        for path in (
            (stage_root / "staging").glob("*.json") if (stage_root / "staging").exists() else ()
        ):
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
        record = {
            "candidate": route,
            "request_id": self._request_id(request),
            "purpose": request.purpose.strip(),
            "route": route,
            "requested_url": fetch.requested_url,
            "final_url": fetch.final_url,
            "source_url": fetch.final_url,
            "content_sha256": digest,
            "status": "duplicate" if duplicate else "success",
            "content_type": content_type,
            "fetched_at": utc_now(),
            "parser_version": f"{route}@m2",
            "robots_decision": robots_decision,
            "policy_decision": "admitted",
            "redirect_chain": list(fetch.redirect_chain),
            "dedupe_decision": "duplicate" if duplicate else "unique",
            "budget": {"max_pages": request.max_pages, "timeout_seconds": request.timeout_seconds},
            "quality": {
                "characters": len(content),
                "title_present": bool(title),
                "discovered_count": discovered_count,
            },
        }
        return IngestionOutcome(
            record["request_id"], route, StageStore(stage_root).stage(record), content
        )

    def ingest(self, request: IngestionRequest, *, stage_root: Path) -> IngestionOutcome:
        target, _ = self.preflight(request)
        if request.mode == "static":
            return self._stage(
                request=request,
                stage_root=stage_root,
                route="trafilatura",
                content=self.static_extractor(target.body),
                title=None,
                fetch=target,
                robots_decision="allowed",
                discovered_count=1,
                content_type=target.headers["Content-Type"],
            )
        if self.browser_handler is None:
            raise IngestionError("browser_route_requires_controlled_firecrawl_handler")
        content, title, final_url, discovered_count = self.browser_handler(request)
        if not 1 <= discovered_count <= request.max_pages:
            raise IngestionError("discovered_count_exceeds_page_budget")
        result_target = validate_target(final_url, policy=TargetPolicy())
        if not result_target.allowed:
            raise IngestionError(f"firecrawl_result_target:{result_target.reason}")
        fetch = HttpFetch(
            target.requested_url,
            result_target.canonical_url,
            200,
            target.headers,
            b"",
            target.redirect_chain,
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
        target = self.http_client.fetch(
            request.url, timeout_seconds=request.timeout_seconds, max_bytes=MAX_RESPONSE_BYTES
        )
        robots = self.http_client.fetch_robots(
            target.final_url, timeout_seconds=min(15.0, request.timeout_seconds)
        )
        if not robots.allowed:
            raise IngestionError(robots.reason)
        if not is_allowed_content_type(target.headers.get("Content-Type")):
            raise IngestionError("content_type_not_allowed")
        return target, robots
