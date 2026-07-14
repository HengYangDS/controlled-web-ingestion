"""Policy-first, body-redacted admission primitives for web ingestion."""

from __future__ import annotations

import ipaddress
import posixpath
import socket
import urllib.robotparser
from dataclasses import dataclass
from typing import Callable, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

INGESTION_AGENT = "ControlledWebIngestion/1.0"
TRACKING_PARAMETERS = frozenset({"fbclid", "gclid", "mc_cid", "mc_eid"})
ALLOWED_CONTENT_TYPES = frozenset({"text/html", "text/plain", "application/pdf"})
FORBIDDEN_PERSISTENCE_FIELDS = frozenset({"body", "content", "html", "markdown", "raw_response"})
STAGE_REQUIRED_FIELDS = frozenset({
    "candidate", "requested_url", "final_url", "source_url", "content_sha256", "status",
    "content_type", "fetched_at", "parser_version", "robots_decision", "policy_decision",
})
STAGE_OPERATIONAL_FIELDS = frozenset({
    "request_id", "purpose", "route", "redirect_chain", "dedupe_decision", "budget", "quality",
})


@dataclass(frozen=True)
class TargetPolicy:
    allowed_schemes: frozenset[str] = frozenset({"http", "https"})


@dataclass(frozen=True)
class TargetDecision:
    allowed: bool
    canonical_url: str
    reason: str


@dataclass(frozen=True)
class RobotsDecision:
    allowed: bool
    reason: str
    crawl_delay_seconds: float | None


class PromotionError(ValueError):
    """A receipt may not cross the staging-to-promotion boundary."""


def canonicalize_url(url: str) -> str:
    """Canonicalize HTTP URL identity without changing semantic query values."""
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    hostname = (parts.hostname or "").lower()
    port = parts.port
    if hostname and port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname
    normalized_path = posixpath.normpath(parts.path or "/")
    if not normalized_path.startswith("/"):
        normalized_path = f"/{normalized_path}"
    if parts.path.endswith("/") and normalized_path != "/":
        normalized_path += "/"
    query_items = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_PARAMETERS
    ]
    return urlunsplit((scheme, netloc, normalized_path, urlencode(sorted(query_items), doseq=True), ""))


def default_resolver(hostname: str) -> list[str]:
    return sorted({record[4][0] for record in socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)})


def _blocked_ip_reason(address: str) -> str | None:
    try:
        value = ipaddress.ip_address(address)
    except ValueError:
        return f"unparseable_resolved_ip:{address}"
    if not value.is_global:
        return f"blocked_ip:{value.compressed}"
    return None


def validate_target(url: str, *, policy: TargetPolicy, resolver: Callable[[str], Iterable[str]] = default_resolver) -> TargetDecision:
    """Reject non-web, credentialed, unresolvable, and non-public targets."""
    canonical_url = canonicalize_url(url)
    parts = urlsplit(canonical_url)
    if parts.scheme not in policy.allowed_schemes:
        return TargetDecision(False, canonical_url, f"blocked_scheme:{parts.scheme or 'missing'}")
    if not parts.hostname:
        return TargetDecision(False, canonical_url, "missing_hostname")
    original = urlsplit(url)
    if original.username or original.password:
        return TargetDecision(False, canonical_url, "embedded_credentials")
    try:
        direct_ip = ipaddress.ip_address(parts.hostname)
    except ValueError:
        try:
            addresses = list(resolver(parts.hostname))
        except OSError as exc:
            return TargetDecision(False, canonical_url, f"dns_error:{type(exc).__name__}")
        if not addresses:
            return TargetDecision(False, canonical_url, "dns_no_addresses")
    else:
        addresses = [str(direct_ip)]
    for address in addresses:
        if reason := _blocked_ip_reason(address):
            return TargetDecision(False, canonical_url, reason)
    return TargetDecision(True, canonical_url, "public_http_target")


def validate_redirect_chain(urls: Iterable[str], *, policy: TargetPolicy, resolver: Callable[[str], Iterable[str]] = default_resolver) -> TargetDecision:
    sequence = list(urls)
    if not sequence:
        return TargetDecision(False, "", "empty_redirect_chain")
    latest = TargetDecision(False, canonicalize_url(sequence[0]), "empty_redirect_chain")
    for target in sequence:
        latest = validate_target(target, policy=policy, resolver=resolver)
        if not latest.allowed:
            return latest
    return latest


def evaluate_robots(robots_text: str, url: str, *, user_agent: str = INGESTION_AGENT) -> RobotsDecision:
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(robots_text.splitlines())
    allowed = parser.can_fetch(user_agent, url)
    delay = parser.crawl_delay(user_agent)
    return RobotsDecision(allowed, "robots_allowed" if allowed else "robots_disallow", float(delay) if delay is not None else None)


def is_allowed_content_type(content_type: str | None) -> bool:
    return bool(content_type) and content_type.split(";", 1)[0].strip().lower() in ALLOWED_CONTENT_TYPES
