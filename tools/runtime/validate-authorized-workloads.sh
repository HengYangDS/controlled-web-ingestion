#!/usr/bin/env bash
# Execute the approved M2-M5 workload set and emit a body-redacted evidence summary.
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
ALLOWLIST="$ROOT/system/policies/authorized-workloads.json"
EVIDENCE="${AGENTIC_EVIDENCE_ROOT:-$ROOT/evidence}/verification/2026-07-14-web-ingestion-m2-m5-validation.json"
PROJECT=web-ingestion-firecrawl-bench
WORK=$(mktemp -d -t web-ingestion-m2-m5.XXXXXX)
STAGE_ROOT="$WORK/stage"
BRIDGE_ROOT="$WORK/bridge"
export UV_NO_MANAGED_PYTHON=1
export UV_PROJECT_ENVIRONMENT="$WORK/python-env"
umask 077

resource_state_is_clean() {
  local containers volumes networks port project_venv
  containers=$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")
  volumes=$(docker volume ls -q --filter "label=com.docker.compose.project=$PROJECT")
  networks=$(docker network ls -q --filter "label=com.docker.compose.project=$PROJECT")
  if [[ -n "$containers" || -n "$volumes" || -n "$networks" ]]; then
    printf 'benchmark Compose resources are not clean\n' >&2
    return 1
  fi
  project_venv=$(find "$ROOT" -type d -name .venv -prune -print -quit 2>/dev/null || true)
  if [[ -n "$project_venv" ]]; then
    printf 'benchmark project virtual environment remains: %s\n' "$project_venv" >&2
    return 1
  fi
  for port in 13002 16379 15672 25672 43691; do
    if lsof -nP -iTCP:"$port" -sTCP:LISTEN | grep -q .; then
      printf 'benchmark port is still listening: %s\n' "$port" >&2
      return 1
    fi
  done
}

cleanup() {
  local status=$?
  trap - EXIT INT TERM
  local cleanup_status=0
  resource_state_is_clean || cleanup_status=1
  rm -rf "$WORK"
  if [[ $status -ne 0 ]]; then
    exit "$status"
  fi
  exit "$cleanup_status"
}
trap cleanup EXIT INT TERM

workload_value() {
  local workload_id=$1
  local field=$2
  python3 - "$ALLOWLIST" "$workload_id" "$field" <<'PY'
import json
import sys

allowlist, workload_id, field = sys.argv[1:]
document = json.load(open(allowlist, encoding="utf-8"))
if document.get("schema") != "web-ingestion-authorized-workloads-v1":
    raise SystemExit("unexpected authorized-workloads schema")
matches = [item for item in document.get("workloads", []) if item.get("id") == workload_id]
if len(matches) != 1 or field not in matches[0]:
    raise SystemExit(f"missing allowlisted workload field: {workload_id}.{field}")
print(matches[0][field])
PY
}

receipt_path() {
  python3 -c 'import json, sys; value = json.load(sys.stdin); print(value["stage_receipt"])'
}

promotion_path() {
  python3 -c 'import json, sys; value = json.load(sys.stdin); print(value["promotion_receipt"])'
}

manifest_path() {
  python3 -c 'import json, sys; value = json.load(sys.stdin); print(value["bridge_manifest"])'
}

assert_receipt() {
  local receipt=$1
  local expected_route=$2
  local expected_status=$3
  local expected_discovered=$4
  python3 - "$receipt" "$expected_route" "$expected_status" "$expected_discovered" <<'PY'
import json
import sys

receipt, route, status, discovered = sys.argv[1:]
record = json.load(open(receipt, encoding="utf-8"))
forbidden = {"body", "content", "html", "markdown", "raw_response"}
present = sorted(forbidden & set(record))
if present:
    raise SystemExit(f"receipt persists forbidden fields: {present}")
if record.get("route") != route or record.get("status") != status:
    raise SystemExit(f"receipt route/status mismatch: {record.get('route')}/{record.get('status')}")
if record.get("policy_decision") != "admitted" or record.get("robots_decision") != "allowed":
    raise SystemExit("receipt was not policy/robots admitted")
if record.get("dedupe_decision") != ("duplicate" if status == "duplicate" else "unique"):
    raise SystemExit("receipt dedupe decision does not match status")
if int(record.get("quality", {}).get("discovered_count", -1)) != int(discovered):
    raise SystemExit("receipt discovery budget/result mismatch")
digest = record.get("content_sha256")
if not isinstance(digest, str) or len(digest) != 64:
    raise SystemExit("receipt has no valid content digest")
PY
}

assert_no_forbidden_persistence() {
  python3 - "$STAGE_ROOT" "$BRIDGE_ROOT" <<'PY'
import json
import sys
from pathlib import Path

for root in map(Path, sys.argv[1:]):
    for path in root.rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        forbidden = {"body", "content", "html", "markdown", "raw_response"} & set(record)
        if forbidden:
            raise SystemExit(f"{path.name} persists forbidden fields: {sorted(forbidden)}")
PY
}

for command in docker lsof python3 uv bash; do
  command -v "$command" >/dev/null || { printf 'missing required command: %s\n' "$command" >&2; exit 2; }
done
[[ -f "$ALLOWLIST" ]] || { printf 'missing authorized workload manifest\n' >&2; exit 2; }
resource_state_is_clean

# Read every value from the allowlist; the script deliberately does not accept
# arbitrary user-supplied URLs as part of its evidence run.
STATIC_ID=static-example-domain
BROWSER_ID=browser-quotes-js
CRAWL_ID=crawl-quotes
STATIC_URL=$(workload_value "$STATIC_ID" url)
STATIC_PURPOSE=$(workload_value "$STATIC_ID" purpose)
STATIC_MODE=$(workload_value "$STATIC_ID" mode)
STATIC_MAX_PAGES=$(workload_value "$STATIC_ID" max_pages)
STATIC_TIMEOUT=$(workload_value "$STATIC_ID" timeout_seconds)
BROWSER_URL=$(workload_value "$BROWSER_ID" url)
BROWSER_PURPOSE=$(workload_value "$BROWSER_ID" purpose)
BROWSER_MODE=$(workload_value "$BROWSER_ID" mode)
BROWSER_MAX_PAGES=$(workload_value "$BROWSER_ID" max_pages)
BROWSER_TIMEOUT=$(workload_value "$BROWSER_ID" timeout_seconds)
CRAWL_URL=$(workload_value "$CRAWL_ID" url)
CRAWL_PURPOSE=$(workload_value "$CRAWL_ID" purpose)
CRAWL_MODE=$(workload_value "$CRAWL_ID" mode)
CRAWL_MAX_PAGES=$(workload_value "$CRAWL_ID" max_pages)
CRAWL_TIMEOUT=$(workload_value "$CRAWL_ID" timeout_seconds)

PROVENANCE=$(python3 "$ROOT/tools/runtime/verify-firecrawl-provenance.py")
printf '%s' "$PROVENANCE" | python3 -c 'import json,sys; assert json.load(sys.stdin).get("status") == "verified"'

STATIC_RECEIPT=$(uv run --locked web-ingest ingest \
  --url "$STATIC_URL" --purpose "$STATIC_PURPOSE" --mode "$STATIC_MODE" \
  --max-pages "$STATIC_MAX_PAGES" --timeout-seconds "$STATIC_TIMEOUT" --stage-root "$STAGE_ROOT" | receipt_path)
assert_receipt "$STATIC_RECEIPT" trafilatura success 1

DUPLICATE_RECEIPT=$(uv run --locked web-ingest ingest \
  --url "$STATIC_URL" --purpose "$STATIC_PURPOSE" --mode "$STATIC_MODE" \
  --max-pages "$STATIC_MAX_PAGES" --timeout-seconds "$STATIC_TIMEOUT" --stage-root "$STAGE_ROOT" | receipt_path)
assert_receipt "$DUPLICATE_RECEIPT" trafilatura duplicate 1

PROMOTED_RECEIPT=$(uv run --locked web-ingest promote \
  --stage-root "$STAGE_ROOT" --receipt "$STATIC_RECEIPT" --confirm | promotion_path)
BRIDGE_MANIFEST=$(uv run --locked web-ingest prepare-rag \
  --bridge-root "$BRIDGE_ROOT" --receipt "$PROMOTED_RECEIPT" --confirm | manifest_path)

BROWSER_RECEIPT=$(uv run --locked web-ingest ingest \
  --url "$BROWSER_URL" --purpose "$BROWSER_PURPOSE" --mode "$BROWSER_MODE" \
  --max-pages "$BROWSER_MAX_PAGES" --timeout-seconds "$BROWSER_TIMEOUT" --stage-root "$STAGE_ROOT" | receipt_path)
assert_receipt "$BROWSER_RECEIPT" firecrawl success 1
resource_state_is_clean

CRAWL_RECEIPT=$(uv run --locked web-ingest ingest \
  --url "$CRAWL_URL" --purpose "$CRAWL_PURPOSE" --mode "$CRAWL_MODE" \
  --max-pages "$CRAWL_MAX_PAGES" --timeout-seconds "$CRAWL_TIMEOUT" --stage-root "$STAGE_ROOT" | receipt_path)
assert_receipt "$CRAWL_RECEIPT" firecrawl success 10
resource_state_is_clean

# Exercise the runner's recovery path directly. The request is deliberately
# private, so the in-run controller must fail and the runner's EXIT trap must
# still release every benchmark resource.
LOOPBACK_REQUEST="$WORK/loopback-request.json"
python3 - "$LOOPBACK_REQUEST" "$WORK/recovery-stage" <<'PY'
import json
import sys

path, stage_root = sys.argv[1:]
with open(path, "w", encoding="utf-8") as handle:
    json.dump({
        "url": "http://127.0.0.1/",
        "purpose": "verify private-target rejection and runner cleanup",
        "mode": "browser",
        "max_pages": 1,
        "timeout_seconds": 30,
        "stage_root": stage_root,
    }, handle)
PY
set +e
bash "$ROOT/tools/runtime/firecrawl-isolated-benchmark.sh" --web-ingest-request "$LOOPBACK_REQUEST" >"$WORK/loopback.stdout" 2>"$WORK/loopback.stderr"
RECOVERY_EXIT=$?
set -e
if [[ $RECOVERY_EXIT -eq 0 ]]; then
  printf 'runner accepted a private web-ingestion request\n' >&2
  exit 1
fi
resource_state_is_clean

assert_no_forbidden_persistence
mkdir -p "$(dirname "$EVIDENCE")"
python3 - "$EVIDENCE" "$ALLOWLIST" "$STATIC_RECEIPT" "$DUPLICATE_RECEIPT" "$BROWSER_RECEIPT" "$CRAWL_RECEIPT" "$PROMOTED_RECEIPT" "$BRIDGE_MANIFEST" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

(
    output,
    allowlist_path,
    static_path,
    duplicate_path,
    browser_path,
    crawl_path,
    promoted_path,
    bridge_path,
) = map(Path, sys.argv[1:])

allowlist = json.loads(allowlist_path.read_text(encoding="utf-8"))
workloads = {item["id"]: item for item in allowlist["workloads"]}
required = {"static-example-domain", "browser-quotes-js", "crawl-quotes"}
if set(workloads) != required:
    raise SystemExit("authorized workload set drifted")

forbidden = {"body", "content", "html", "markdown", "raw_response"}
def load(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    persisted = forbidden & set(value)
    if persisted:
        raise SystemExit(f"{path.name} contains forbidden fields: {sorted(persisted)}")
    return value

def receipt_summary(path):
    record = load(path)
    return {
        key: record[key]
        for key in (
            "request_id", "purpose", "route", "requested_url", "final_url", "source_url",
            "content_sha256", "status", "content_type", "robots_decision", "policy_decision",
            "redirect_chain", "dedupe_decision", "budget", "quality", "promotion_state",
        )
    }

promoted = load(promoted_path)
bridge = load(bridge_path)
if promoted.get("promotion_state") != "promoted":
    raise SystemExit("promotion receipt is not promoted")
if bridge.get("bridge_state") != "prepared" or bridge.get("sink") is not None:
    raise SystemExit("bridge manifest is not default-disabled")

summary = {
    "schema": "web-ingestion-m2-m5-validation-v1",
    "executed_at": datetime.now(timezone.utc).isoformat(),
    "authorized_workloads": [
        {key: item[key] for key in ("id", "url", "purpose", "mode", "max_pages", "timeout_seconds")}
        for item in allowlist["workloads"]
    ],
    "provenance": {"status": "verified"},
    "receipts": {
        "static": receipt_summary(static_path),
        "duplicate_static": receipt_summary(duplicate_path),
        "browser": receipt_summary(browser_path),
        "crawl": receipt_summary(crawl_path),
    },
    "promotion": {
        key: promoted[key]
        for key in ("promotion_state", "content_sha256", "source_url", "purpose", "route", "status")
    },
    "rag_bridge": {
        key: bridge[key]
        for key in ("bridge_state", "content_sha256", "source_url", "purpose", "sink")
    },
    "recovery": {
        "private_loopback_runner_exit_nonzero": True,
        "cleanup_after_failure_verified": True,
    },
    "cleanup": {
        "containers": 0,
        "volumes": 0,
        "networks": 0,
        "benchmark_listeners": 0,
        "project_virtualenvs": 0,
    },
    "limits": [
        "body_html_markdown_and_raw_response_not_persisted",
        "rag_bridge_sink_is_null",
        "firecrawl_is_on_demand_and_loopback_only",
        "no_mcp_default_agent_hermes_or_open_webui_integration",
    ],
}
temporary = output.with_suffix(output.suffix + ".tmp")
temporary.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
temporary.replace(output)
PY

printf 'M2-M5 body-redacted validation evidence written: %s\n' "$EVIDENCE"
