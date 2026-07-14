#!/usr/bin/env python3
"""Fail when runtime, system truth, tool or test ownership drift."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    failures: list[str] = []
    for path in ROOT.glob("*.py"):
        failures.append(f"root implementation module is forbidden: {path.name}")
    for forbidden in (ROOT / "scripts", ROOT / "ops", ROOT / "policy.json"):
        if forbidden.exists():
            failures.append(f"legacy topology root remains: {forbidden.relative_to(ROOT)}")
    for required in (
        ROOT / "src" / "web_ingestion",
        ROOT / "system" / "policies",
        ROOT / "system" / "projections",
        ROOT / "system" / "supply-chain",
        ROOT / "system" / "schemas",
        ROOT / "tools" / "benchmark",
        ROOT / "tools" / "ci",
        ROOT / "tools" / "runtime",
        ROOT / "tools" / "supply-chain",
        ROOT / "tests" / "unit",
        ROOT / "tests" / "contract",
        ROOT / "tests" / "integration",
    ):
        if not required.is_dir():
            failures.append(f"required topology root missing: {required.relative_to(ROOT)}")
    for path in (ROOT / "src" / "web_ingestion").rglob("*.py"):
        content = path.read_text(encoding="utf-8")
        if "tools.benchmark" in content or "run_framework_comparison" in content:
            failures.append(f"runtime package imports benchmark lane: {path.relative_to(ROOT)}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("source topology validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
