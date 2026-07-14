#!/usr/bin/env bash
# Bind Python and uv transient state to ignored semantic runtime homes.
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
PYTHON_BIN=${1:?usage: with-python-runtime.sh <python> <command> [args...]}
shift
export UV_CACHE_DIR="${UV_CACHE_DIR:-$ROOT/build/runtime/tool-cache/uv}"
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-$ROOT/build/runtime/venv/python-${PYTHON_BIN##*/}}"
mkdir -p "$UV_CACHE_DIR" "$(dirname "$UV_PROJECT_ENVIRONMENT")"
exec uv run --locked --python "$PYTHON_BIN" "$@"
