#!/usr/bin/env bash
# Run a disposable, loopback-only Firecrawl M1 validation and always clean it up.
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
COMPOSE_FILE="$ROOT/system/projections/firecrawl-isolated-compose.yaml"
EVIDENCE_DIR="$ROOT/results/m1"
PROJECT=web-ingestion-firecrawl-bench
WORK=$(mktemp -d -t web-ingestion-firecrawl.XXXXXX)
REDIS_PID=""
RABBIT_PID=""
EPMD_PID=""
COMPOSE_STARTED=0
WEB_INGEST_REQUEST=""
umask 077

cleanup() {
  status=$?
  # A signal and the EXIT trap can otherwise enter cleanup twice. Disable both
  # before tearing down this run's exclusively preflighted resources.
  trap - EXIT INT TERM
  if (( COMPOSE_STARTED )); then
    docker compose --project-name "$PROJECT" --env-file "$WORK/firecrawl.env" -f "$COMPOSE_FILE" down --volumes --remove-orphans >/dev/null 2>&1 || true
  fi
  [[ -n "$RABBIT_PID" ]] && kill "$RABBIT_PID" >/dev/null 2>&1 || true
  [[ -n "$REDIS_PID" ]] && kill "$REDIS_PID" >/dev/null 2>&1 || true
  wait "${RABBIT_PID:-}" >/dev/null 2>&1 || true
  wait "${REDIS_PID:-}" >/dev/null 2>&1 || true
  if [[ -z "$EPMD_PID" ]]; then
    EPMD_PID=$(lsof -t -nP -iTCP:43691 -sTCP:LISTEN 2>/dev/null || true)
  fi
  for pid in ${EPMD_PID:-}; do
    kill "$pid" >/dev/null 2>&1 || true
  done
  rm -rf "$WORK"
  exit "$status"
}
trap cleanup EXIT INT TERM

if [[ $# -gt 0 ]]; then
  if [[ $# -ne 2 || "$1" != "--web-ingest-request" || ! -f "$2" ]]; then
    printf 'usage: %s [--web-ingest-request <request-json>]\n' "$0" >&2
    exit 2
  fi
  WEB_INGEST_REQUEST=$(cd "$(dirname "$2")" && pwd)/$(basename "$2")
fi

for command in docker redis-server rabbitmq-server uv curl lsof python3; do
  command -v "$command" >/dev/null || { printf 'missing required command: %s\n' "$command" >&2; exit 2; }
done

# Resolve the lockfile from the experiment itself even when this runner is
# called by absolute path. The virtual environment remains inside WORK and is
# removed by the trap with all other disposable runtime state.
cd "$ROOT"
export UV_NO_MANAGED_PYTHON=1
export UV_PROJECT_ENVIRONMENT="$WORK/python-env"
python3 "$ROOT/tools/runtime/verify-firecrawl-provenance.py"

if docker ps -aq --filter "label=com.docker.compose.project=$PROJECT" | grep -q .; then
  printf 'refusing to touch an existing %s project\n' "$PROJECT" >&2
  exit 2
fi
if lsof -nP -iTCP:13002 -sTCP:LISTEN | grep -q . || lsof -nP -iTCP:16379 -sTCP:LISTEN | grep -q . || lsof -nP -iTCP:15672 -sTCP:LISTEN | grep -q . || lsof -nP -iTCP:25672 -sTCP:LISTEN | grep -q . || lsof -nP -iTCP:43691 -sTCP:LISTEN | grep -q .; then
  printf 'one or more benchmark-only loopback ports are already in use\n' >&2
  exit 2
fi

cat >"$WORK/rabbitmq.conf" <<'EOF'
listeners.tcp.1 = 127.0.0.1:15672
loopback_users.guest = true
# The Homebrew service enables management/STOMP/AMQP 1.0/MQTT/stream plugins
# globally. This temporary benchmark needs only core AMQP, so override that
# generated plugin set before launching RabbitMQ; no service setting is changed.
management.tcp.port = 0
stomp.listeners.tcp = none
mqtt.listeners.tcp = none
stream.listeners.tcp = none
distribution.listener.interface = 127.0.0.1
distribution.listener.port_range.min = 25672
distribution.listener.port_range.max = 25672
EOF
cat >"$WORK/firecrawl.env" <<EOF
POSTGRES_USER=firecrawl_bench
POSTGRES_PASSWORD=$(openssl rand -hex 24)
POSTGRES_DB=postgres
BULL_AUTH_KEY=$(openssl rand -hex 24)
EOF

redis-server --bind 127.0.0.1 --port 16379 --save '' --appendonly no --dir "$WORK" >"$WORK/redis.log" 2>&1 &
REDIS_PID=$!
printf '%s\n' '[] .' >"$WORK/enabled_plugins"
RABBITMQ_NODENAME="firecrawl_bench_${RANDOM}_$$" \
RABBITMQ_ENABLED_PLUGINS_FILE="$WORK/enabled_plugins" \
RABBITMQ_CONFIG_FILE="$WORK/rabbitmq" \
RABBITMQ_MNESIA_BASE="$WORK/rabbit-mnesia" \
RABBITMQ_LOG_BASE="$WORK/rabbit-log" \
RABBITMQ_PID_FILE="$WORK/rabbit.pid" \
ERL_EPMD_ADDRESS=127.0.0.1 \
ERL_EPMD_PORT=43691 \
rabbitmq-server >"$WORK/rabbitmq.log" 2>&1 &
RABBIT_PID=$!

for _ in $(seq 1 60); do
  if redis-cli -h 127.0.0.1 -p 16379 ping 2>/dev/null | grep -qx PONG && lsof -nP -iTCP:15672 -sTCP:LISTEN | grep -Eq 'TCP (127\.0\.0\.1|\[::1\]):15672'; then
    break
  fi
  if ! kill -0 "$RABBIT_PID" 2>/dev/null; then
    cat "$WORK/rabbitmq.log" >&2 || true
    exit 1
  fi
  sleep 1
done
redis-cli -h 127.0.0.1 -p 16379 ping | grep -qx PONG
lsof -nP -iTCP:15672 -sTCP:LISTEN | grep -Eq 'TCP (127\.0\.0\.1|\[::1\]):15672'
EPMD_PID=$(lsof -t -nP -iTCP:43691 -sTCP:LISTEN)
for port in 5552 61613 1883; do
  if lsof -nP -iTCP:"$port" -sTCP:LISTEN | grep -q .; then
    printf 'RabbitMQ unexpected optional plugin listener on port %s\n' "$port" >&2
    exit 1
  fi
done

mkdir -p "$EVIDENCE_DIR"
COMPOSE_STARTED=1
if [[ -n "$WEB_INGEST_REQUEST" ]]; then
  docker compose --project-name "$PROJECT" --env-file "$WORK/firecrawl.env" -f "$COMPOSE_FILE" up --detach >/dev/null
else
  docker compose --project-name "$PROJECT" --env-file "$WORK/firecrawl.env" -f "$COMPOSE_FILE" up --detach
fi

for _ in $(seq 1 90); do
  status=$(curl --silent --output /dev/null --write-out '%{http_code}' --max-time 3 http://127.0.0.1:13002/ || true)
  if [[ "$status" != "000" && -n "$status" ]]; then
    break
  fi
  sleep 1
done
status=$(curl --silent --output /dev/null --write-out '%{http_code}' --max-time 5 http://127.0.0.1:13002/ || true)
[[ "$status" != "000" && -n "$status" ]]

export FIRECRAWL_ENDPOINT=http://127.0.0.1:13002
if [[ -n "$WEB_INGEST_REQUEST" ]]; then
  uv run --locked web-ingest --internal-firecrawl-stage "$WEB_INGEST_REQUEST"
  exit 0
fi
for case_name in static javascript crawl; do
  uv run --locked python "$ROOT/tools/benchmark/run_framework_comparison.py" --candidate firecrawl --case "$case_name" --output "$EVIDENCE_DIR/firecrawl-$case_name.json"
done

uv run --locked python - <<'PY' >"$EVIDENCE_DIR/firecrawl-ssrf.json"
from __future__ import annotations
import hashlib
import json
import urllib.error
import urllib.request

payload = json.dumps({"url": "http://127.0.0.1:3002/", "formats": ["markdown"]}).encode()
request = urllib.request.Request(
    "http://127.0.0.1:13002/v1/scrape",
    data=payload,
    method="POST",
    headers={"Content-Type": "application/json"},
)
try:
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read()
        status = response.status
except urllib.error.HTTPError as exc:
    body = exc.read()
    status = exc.code
    record = {
        "request_target": "loopback",
        "status_code": status,
        "response_sha256": hashlib.sha256(body).hexdigest(),
        "rejected": True,
    }
except Exception as exc:
    record = {
        "request_target": "loopback",
        "transport_error": type(exc).__name__,
        "rejected": True,
    }
else:
    record = {
        "request_target": "loopback",
        "status_code": status,
        "response_sha256": hashlib.sha256(body).hexdigest(),
        "rejected": False,
    }
print(json.dumps(record, sort_keys=True))
if not record["rejected"]:
    raise SystemExit("Firecrawl accepted a loopback scrape target")
PY

docker compose --project-name "$PROJECT" --env-file "$WORK/firecrawl.env" -f "$COMPOSE_FILE" ps --format json >"$EVIDENCE_DIR/firecrawl-services.json"
docker stats --no-stream --format '{{json .}}' $(docker compose --project-name "$PROJECT" --env-file "$WORK/firecrawl.env" -f "$COMPOSE_FILE" ps -q) >"$EVIDENCE_DIR/firecrawl-resources.jsonl"
lsof -nP -iTCP -sTCP:LISTEN | grep -E ':(13002|16379|15672|25672|43691) ' >"$EVIDENCE_DIR/firecrawl-listeners.txt"
if grep -Ev 'TCP (127\.0\.0\.1|\[::1\]):' "$EVIDENCE_DIR/firecrawl-listeners.txt" | grep -q .; then
  printf 'benchmark listener escaped loopback scope\n' >&2
  exit 1
fi
docker image inspect \
  ghcr.io/firecrawl/firecrawl:2.10.19 \
  ghcr.io/firecrawl/playwright-service:latest \
  ghcr.io/firecrawl/nuq-postgres:latest \
  >"$EVIDENCE_DIR/firecrawl-image-inspect.json"

printf '%s\n' "Firecrawl M1 result records written under $EVIDENCE_DIR; teardown now begins."
