"""Bounded, redirect-aware public HTTP transport."""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable
from urllib.parse import urljoin, urlsplit

from .contracts import HttpFetch, IngestionError, RawHttpResponse
from .policy import INGESTION_AGENT, TargetPolicy, evaluate_robots, validate_target


def default_transport(url: str, *, timeout_seconds: float, max_bytes: int) -> RawHttpResponse:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
            return None

    request = urllib.request.Request(url, headers={"User-Agent": INGESTION_AGENT})
    opener = urllib.request.build_opener(NoRedirect)
    try:
        response = opener.open(request, timeout=timeout_seconds)  # noqa: S310 - admission validates target first
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        return RawHttpResponse(
            url=response.geturl(),
            status_code=response.status,
            headers={key: value for key, value in response.headers.items()},
            body=response.read(max_bytes + 1),
        )


class SafeHttpClient:
    """Fetch public HTTP(S) targets one hop at a time after policy admission."""

    def __init__(
        self,
        *,
        resolver: Callable[[str], Iterable[str]] | None = None,
        transport: Callable[..., RawHttpResponse] = default_transport,
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
                chain[0],
                current,
                response.status_code,
                response.headers,
                response.body,
                tuple(chain),
            )
        raise IngestionError("redirect_limit_exceeded")

    def fetch_robots(self, url: str, *, timeout_seconds: float):
        parts = urlsplit(url)
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        try:
            response = self.fetch(robots_url, timeout_seconds=timeout_seconds, max_bytes=256 * 1024)
        except IngestionError as exc:
            if str(exc) == "http_status:404":
                return evaluate_robots("", url, user_agent=INGESTION_AGENT)
            raise IngestionError(f"robots_unavailable:{exc}") from exc
        return evaluate_robots(
            response.body.decode("utf-8", errors="replace"), url, user_agent=INGESTION_AGENT
        )
