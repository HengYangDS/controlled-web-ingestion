#!/usr/bin/env python3
"""Run a disposable Compose command in an isolated process group with a hard bound."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid-file", type=Path)
    parser.add_argument("--timeout-seconds", type=float, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if args.timeout_seconds <= 0 or not command:
        parser.error("a positive timeout and command are required")
    process = subprocess.Popen(command, start_new_session=True)
    if args.pid_file is not None:
        args.pid_file.write_text(f"{process.pid}\n", encoding="utf-8")
    try:
        return process.wait(timeout=args.timeout_seconds)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        print(f"bounded Compose command exceeded {args.timeout_seconds:g} seconds", file=sys.stderr)
        return 124
    finally:
        if args.pid_file is not None:
            args.pid_file.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
