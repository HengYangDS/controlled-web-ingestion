#!/usr/bin/env python3
"""Render both Forge pipelines from the CUE model, or report the ones that drifted."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = ".config/ci/pipeline.cue"
PROJECTIONS = {
    "github": Path(".github/workflows/verify.yml"),
    "gitlab": Path(".gitlab-ci.yml"),
}


def cue_executable() -> str:
    """Return the CUE on PATH once it is the version that the mise configuration locks."""
    tools = tomllib.loads((ROOT / ".config/mise/config.toml").read_text(encoding="utf-8"))
    version = tools["tools"]["cue"]
    cue = shutil.which("cue")
    if cue is None:
        raise SystemExit("cue is not on PATH; run `mise run bootstrap`")
    observed = subprocess.run(
        (cue, "version"), check=True, capture_output=True, text=True, stdin=subprocess.DEVNULL
    ).stdout
    if not observed.startswith(f"cue version v{version}\n"):
        raise SystemExit(f"cue {version} is required; run the check through `mise run check`")
    return cue


def render(cue: str, expression: str) -> bytes:
    """Export one projection from the model alone, without any CUE module or registry."""
    command = (cue, "export", MODEL, "--expression", expression, "--out", "yaml")
    result = subprocess.run(
        command, cwd=ROOT, check=True, capture_output=True, stdin=subprocess.DEVNULL
    )
    return result.stdout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail when a projection differs")
    mode.add_argument("--write", action="store_true", help="write every projection")
    args = parser.parse_args(argv)
    cue = cue_executable()
    drifted = []
    for expression, relative in PROJECTIONS.items():
        expected = render(cue, expression)
        path = ROOT / relative
        if args.write:
            path.write_bytes(expected)
        elif not path.is_file() or path.read_bytes() != expected:
            drifted.append(relative.as_posix())
    for relative in drifted:
        print(f"{relative} differs from {MODEL}; run `mise run fix`", file=sys.stderr)
    return 1 if drifted else 0


if __name__ == "__main__":
    raise SystemExit(main())
