#!/bin/sh
# Scan the checked-out tree with the required secret detector; do not mutate it.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$ROOT"
command -v gitleaks >/dev/null 2>&1 || { echo 'gitleaks is required for the security gate' >&2; exit 2; }
gitleaks git --no-banner --redact=100 --exit-code 1 .
