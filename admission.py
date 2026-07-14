"""Policy-first, body-redacted admission primitives for web ingestion.

This module deliberately decides whether a target may be fetched and whether a
redacted result may be promoted.  It neither fetches pages nor writes to RAG,
MCP, or agent-tool registries.
"""

from __future__ import annotations

import hashlib
import ipaddress
import json
import posixpath
import socket
import urllib.robotparser
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


BENCHMARK_AGENT = "AgenticWebIngestionBenchmark"
TRACKING_PARAMETERS = frozenset({"fbclid", "gclid", "mc_cid", "mc_eid"})
ALLOWED_CONTENT_TYPES = frozenset({"text/html", "text/plain", "application/pdf"})
FORBIDDEN_PERSISTENCE_FIELDS = frozenset({"body", "content", "html", "markdown", "raw_response"})
STAGE_REQUIRED_FIELDS = frozenset({
    "candidate",
    "requested_url",
    "final_url",
    "source_url",
    "content_sha256",
    "status",
    "content_type",
    "fetched_at",
    "parser_version",
    "robots_decision",
    "policy_decision",
})
STAGE_OPERATIONAL_FIELDS = frozenset({
    "request_id",
    "purpose",
    "route",
    "redirect_chain",
    "dedupe_decision",
    "budget",
    "quality",
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
    """Raised when an item cannot cross the staging-to-promotion boundary."""


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
    query = urlencode(sorted(query_items), doseq=True)
    return urlunsplit((scheme, netloc, normalized_path, query, ""))


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


def validate_target(
    url: str,
    *,
    policy: TargetPolicy,
    resolver: Callable[[str], Iterable[str]] = default_resolver,
) -> TargetDecision:
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
        reason = _blocked_ip_reason(address)
        if reason:
            return TargetDecision(False, canonical_url, reason)
    return TargetDecision(True, canonical_url, "public_http_target")


def validate_redirect_chain(
    urls: Iterable[str],
    *,
    policy: TargetPolicy,
    resolver: Callable[[str], Iterable[str]] = default_resolver,
) -> TargetDecision:
    """Validate every redirect target, so a public initial URL cannot pivot inward."""
    sequence = list(urls)
    if not sequence:
        return TargetDecision(False, "", "empty_redirect_chain")
    latest = TargetDecision(False, canonicalize_url(sequence[0]), "empty_redirect_chain")
    for target in sequence:
        latest = validate_target(target, policy=policy, resolver=resolver)
        if not latest.allowed:
            return latest
    return latest


def evaluate_robots(robots_text: str, url: str, *, user_agent: str = BENCHMARK_AGENT) -> RobotsDecision:
    """Evaluate robots text and preserve crawl-delay as a policy result."""
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(robots_text.splitlines())
    allowed = parser.can_fetch(user_agent, url)
    delay = parser.crawl_delay(user_agent)
    return RobotsDecision(
        allowed=allowed,
        reason="robots_allowed" if allowed else "robots_disallow",
        crawl_delay_seconds=float(delay) if delay is not None else None,
    )


def is_allowed_content_type(content_type: str | None) -> bool:
    if not content_type:
        return False
    media_type = content_type.split(";", 1)[0].strip().lower()
    return media_type in ALLOWED_CONTENT_TYPES


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_stage_record(record: dict[str, object]) -> None:
    missing = sorted(STAGE_REQUIRED_FIELDS - record.keys())
    if missing:
        raise PromotionError(f"stage record missing fields: {', '.join(missing)}")
    forbidden = sorted(FORBIDDEN_PERSISTENCE_FIELDS & record.keys())
    if forbidden:
        raise PromotionError(f"stage record has forbidden fields: {', '.join(forbidden)}")
    digest = record.get("content_sha256")
    if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise PromotionError("stage record needs a lowercase SHA-256 content digest")
    if "route" in record:
        operational_missing = sorted(STAGE_OPERATIONAL_FIELDS - record.keys())
        if operational_missing:
            raise PromotionError(f"operational stage record missing fields: {', '.join(operational_missing)}")
        if not isinstance(record.get("purpose"), str) or not str(record["purpose"]).strip():
            raise PromotionError("operational stage record needs a non-empty purpose")


class StageStore:
    """A filesystem-only staging ledger with explicit, non-RAG promotion."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.staging_dir = root / "staging"
        self.promotion_dir = root / "promoted"

    def stage(self, record: dict[str, object]) -> Path:
        _validate_stage_record(record)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        persisted = dict(record)
        persisted["promotion_state"] = "staged"
        persisted["staged_at"] = _utc_now()
        normalized = json.dumps(persisted, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        identity = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        path = self.staging_dir / f"{identity}.json"
        path.write_text(json.dumps(persisted, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def promote(self, stage_path: Path, *, explicit_confirmation: bool) -> Path:
        if not explicit_confirmation:
            raise PromotionError("explicit confirmation is required for promotion")
        try:
            record = json.loads(stage_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PromotionError(f"cannot read staged record: {type(exc).__name__}") from exc
        if not isinstance(record, dict):
            raise PromotionError("staged record must be a JSON object")
        _validate_stage_record(record)
        if record.get("promotion_state") != "staged":
            raise PromotionError("only staged records may be promoted")
        if record.get("status") != "success":
            raise PromotionError("only successful records may be promoted")
        if record.get("dedupe_decision") == "duplicate":
            raise PromotionError("duplicate content may not be promoted")
        if record.get("policy_decision") != "admitted":
            raise PromotionError("policy must admit the record before promotion")
        if record.get("robots_decision") != "allowed":
            raise PromotionError("robots policy must allow the record before promotion")
        if not is_allowed_content_type(str(record.get("content_type"))):
            raise PromotionError("content type is not eligible for promotion")
        self.promotion_dir.mkdir(parents=True, exist_ok=True)
        record["promotion_state"] = "promoted"
        record["promoted_at"] = _utc_now()
        output = self.promotion_dir / stage_path.name
        output.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return output
