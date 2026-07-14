#!/usr/bin/env python3
"""Run the full layered test suite with the selected interpreter."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _runtime_python(command: str) -> str:
    """Resolve a selected interpreter inside the active uv project environment.

    `uv run` exposes its environment through PATH.  Re-invoking the host
    interpreter would bypass the editable project installation, so the owner
    command launches child test processes with the active environment's Python.
    """
    active = Path(sys.executable)
    return str(active) if active.exists() else command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args(argv)
    runtime_python = _runtime_python(args.python)
    commands = [
        [runtime_python, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"],
        ["bash", "-n", str(ROOT / "tools" / "runtime" / "firecrawl-isolated-benchmark.sh")],
        ["bash", "-n", str(ROOT / "tools" / "runtime" / "validate-authorized-workloads.sh")],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
