#!/usr/bin/env python3
"""Validate reviewed system declarations and all committed redacted evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from web_ingestion.schema import load_named_schema, validate_document  # noqa: E402

DECLARATIONS = {
    ROOT / "system" / "policies" / "ingestion-policy.json": "ingestion-policy",
    ROOT / "system" / "policies" / "authorized-workloads.json": "authorized-workloads",
    ROOT / "system" / "projections" / "routing.json": "routing",
}


def main() -> int:
    failures: list[str] = []
    for path, schema_name in DECLARATIONS.items():
        document = json.loads(path.read_text(encoding="utf-8"))
        failures.extend(f"{path.relative_to(ROOT)}: {error}" for error in validate_document(document, load_named_schema(schema_name)))
    for path in sorted((ROOT / "evidence").rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        failures.extend(f"{path.relative_to(ROOT)}: {error}" for error in validate_document(document, load_named_schema("evidence")))
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(json.dumps({"status": "validated", "declarations": len(DECLARATIONS), "evidence": len(list((ROOT / 'evidence').rglob('*.json')))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
