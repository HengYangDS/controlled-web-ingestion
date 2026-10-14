"""Validate the reviewed authorized workload set end to end and record body-redacted evidence."""

from __future__ import annotations

import hashlib
import json
import tempfile
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .bridge import RagBridge
from .contracts import IngestionError, IngestionRequest
from .controller import IngestionController
from .runtime import (
    COMPOSE_FILE,
    PROVENANCE_FILE,
    ROOT,
    firecrawl_runtime,
    project_resources,
    published_ports,
    stage_with_firecrawl,
    verify_reviewed_images,
)
from .staging import StageStore

ALLOWLIST = ROOT / "system" / "policies" / "authorized-workloads.json"
ALLOWLIST_SCHEMA = "web-ingestion-authorized-workloads-v1"
EVIDENCE_SCHEMA = "controlled-web-ingestion-runtime-validation-v2"
WORKLOAD_IDS = frozenset({"static-example-domain", "browser-quotes-js", "crawl-quotes"})
FORBIDDEN = frozenset({"body", "content", "html", "markdown", "raw_response"})
RECEIPT_FIELDS = (
    "request_id",
    "purpose",
    "route",
    "requested_url",
    "final_url",
    "source_url",
    "content_sha256",
    "status",
    "content_type",
    "robots_decision",
    "policy_decision",
    "redirect_chain",
    "dedupe_decision",
    "budget",
    "quality",
    "promotion_state",
)
LIMITS = (
    "body_html_markdown_and_raw_response_not_persisted",
    "rag_bridge_sink_is_null",
    "firecrawl_is_on_demand_and_loopback_only",
    "no_mcp_default_agent_hermes_or_open_webui_integration",
)


class ValidationFailure(RuntimeError):
    """A reviewed workload, receipt, isolation or cleanup check did not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def load_workloads(path: Path = ALLOWLIST) -> dict[str, dict[str, Any]]:
    """Read only the reviewed allowlist and refuse any drift in its workload set."""
    document = json.loads(path.read_text(encoding="utf-8"))
    _require(document.get("schema") == ALLOWLIST_SCHEMA, "unexpected authorized-workloads schema")
    workloads = {item["id"]: item for item in document.get("workloads", [])}
    _require(set(workloads) == WORKLOAD_IDS, "authorized workload set drifted")
    return workloads


def request_for(workload: dict[str, Any]) -> IngestionRequest:
    return IngestionRequest(
        url=workload["url"],
        purpose=workload["purpose"],
        mode=workload["mode"],
        max_pages=int(workload["max_pages"]),
        timeout_seconds=float(workload["timeout_seconds"]),
    )


def load_redacted(path: Path) -> dict[str, Any]:
    record = json.loads(path.read_text(encoding="utf-8"))
    present = sorted(FORBIDDEN & set(record))
    _require(not present, f"{path.name} persists forbidden fields: {present}")
    return record


def assert_receipt(path: Path, *, route: str, status: str, discovered: int) -> dict[str, Any]:
    """Check one staging receipt and return its body-redacted summary."""
    record = load_redacted(path)
    _require(
        record.get("route") == route and record.get("status") == status,
        f"receipt route/status mismatch: {record.get('route')}/{record.get('status')}",
    )
    _require(
        record.get("policy_decision") == "admitted" and record.get("robots_decision") == "allowed",
        "receipt was not policy/robots admitted",
    )
    _require(
        record.get("dedupe_decision") == ("duplicate" if status == "duplicate" else "unique"),
        "receipt dedupe decision does not match status",
    )
    _require(
        int(record.get("quality", {}).get("discovered_count", -1)) == discovered,
        "receipt discovery budget/result mismatch",
    )
    digest = record.get("content_sha256")
    _require(isinstance(digest, str) and len(digest) == 64, "receipt has no valid content digest")
    return {key: record[key] for key in RECEIPT_FIELDS}


def assert_no_forbidden_persistence(*roots: Path) -> None:
    for root in roots:
        for path in root.rglob("*.json"):
            load_redacted(path)


def service_rejects_loopback(endpoint: str) -> dict[str, Any]:
    """Ask the running service itself to scrape a loopback address; it must refuse."""
    request = urllib.request.Request(
        f"{endpoint}/v1/scrape",
        data=json.dumps({"url": "http://127.0.0.1:3002/", "formats": ["markdown"]}).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310 - loopback API
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code
    except OSError as error:
        return {"target": "loopback", "transport_error": type(error).__name__, "rejected": True}
    return {"target": "loopback", "status_code": status, "rejected": status >= 400}


def _unexpected_browser_call(_request: IngestionRequest) -> tuple[str, str | None, str, int]:
    raise ValidationFailure("a private request reached the Firecrawl handler")


def _recovery(stage_root: Path) -> dict[str, Any]:
    """Fail one staged request inside a running topology and keep the isolation facts."""
    private = IngestionRequest(
        url="http://127.0.0.1/",
        purpose="verify private-target rejection and runtime cleanup",
        mode="browser",
        max_pages=1,
        timeout_seconds=30,
    )
    observed: dict[str, Any] = {}
    try:
        with firecrawl_runtime() as endpoint:
            observed["published_ports"] = published_ports()
            observed["service_loopback_scrape"] = service_rejects_loopback(endpoint)
            IngestionController(browser_handler=_unexpected_browser_call).ingest(
                private, stage_root=stage_root
            )
    except IngestionError as error:
        observed["in_run_rejection"] = str(error)
    _require("in_run_rejection" in observed, "the runtime staged a private request")
    _require(observed["published_ports"] == ["127.0.0.1:13002"], "a listener escaped loopback")
    _require(observed["service_loopback_scrape"]["rejected"], "Firecrawl accepted loopback")
    return observed


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_authorized_workloads(evidence: Path) -> Path:
    """Run the reviewed workloads, then write one evidence record only if every check holds."""
    workloads = load_workloads()
    images = verify_reviewed_images()
    initial = project_resources()
    _require(not any(initial.values()), f"benchmark resources are not clean: {initial}")
    with tempfile.TemporaryDirectory(prefix="web-ingestion-validation-") as work:
        stage, bridge, recovery = (Path(work) / name for name in ("stage", "bridge", "recovery"))
        static = request_for(workloads["static-example-domain"])
        controller = IngestionController()
        static_receipt = controller.ingest(static, stage_root=stage).stage_receipt
        duplicate_receipt = controller.ingest(static, stage_root=stage).stage_receipt
        receipts = {
            "static": assert_receipt(
                static_receipt, route="trafilatura", status="success", discovered=1
            ),
            "duplicate_static": assert_receipt(
                duplicate_receipt, route="trafilatura", status="duplicate", discovered=1
            ),
        }
        promoted_path = StageStore(stage).promote(static_receipt, explicit_confirmation=True)
        bridge_path = RagBridge(bridge).prepare(promoted_path, explicit_confirmation=True)
        for label, workload_id, discovered in (
            ("browser", "browser-quotes-js", 1),
            ("crawl", "crawl-quotes", 10),
        ):
            request = request_for(workloads[workload_id])
            controller.preflight(request)
            outcome = stage_with_firecrawl(request, stage)
            receipts[label] = assert_receipt(
                outcome.stage_receipt, route="firecrawl", status="success", discovered=discovered
            )
        isolation = _recovery(recovery)
        cleanup = project_resources()
        _require(not any(cleanup.values()), f"benchmark resources remain: {cleanup}")
        assert_no_forbidden_persistence(stage, bridge, recovery)
        promoted = load_redacted(promoted_path)
        manifest = load_redacted(bridge_path)
        _require(promoted.get("promotion_state") == "promoted", "promotion receipt is not promoted")
        _require(
            manifest.get("bridge_state") == "prepared" and manifest.get("sink") is None,
            "bridge manifest is not default-disabled",
        )
    summary = {
        "schema": EVIDENCE_SCHEMA,
        "executed_at": datetime.now(UTC).isoformat(),
        "status": "passed",
        "declarations": {
            path.relative_to(ROOT).as_posix(): _sha256(path)
            for path in (COMPOSE_FILE, PROVENANCE_FILE, ALLOWLIST)
        },
        "images": images,
        "authorized_workloads": [
            {key: item[key] for key in ("id", "url", "purpose", "mode", "max_pages")}
            for item in workloads.values()
        ],
        "receipts": receipts,
        "promotion": {
            key: promoted[key]
            for key in ("promotion_state", "content_sha256", "source_url", "purpose", "route")
        },
        "rag_bridge": {
            key: manifest[key]
            for key in ("bridge_state", "content_sha256", "source_url", "purpose", "sink")
        },
        "isolation": isolation,
        "cleanup": cleanup,
        "limits": list(LIMITS),
    }
    evidence.parent.mkdir(parents=True, exist_ok=True)
    temporary = evidence.with_suffix(evidence.suffix + ".tmp")
    temporary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(evidence)
    return evidence
