#!/usr/bin/env python3
"""Validate the canonical documentation kernel and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ("architecture", "decisions", "evidence", "reference", "start", "plans")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def has_required_front_matter(path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError:
        return False
    fields = {line.split(":", 1)[0] for line in lines[1:end] if ":" in line}
    return {"subject", "role", "state", "relations"} <= fields


def main() -> int:
    failures: list[str] = []
    docs = ROOT / "docs"
    paths: list[Path] = []
    for name in CANONICAL:
        directory = docs / name
        if not directory.is_dir():
            failures.append(f"canonical documentation root missing: docs/{name}")
            continue
        paths.extend(directory.rglob("*.md"))
    for path in sorted(paths):
        if not has_required_front_matter(path):
            failures.append(f"canonical document lacks complete front matter: {path.relative_to(ROOT)}")
        for href in LINK.findall(path.read_text(encoding="utf-8")):
            target = href.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                failures.append(f"broken local link in {path.relative_to(ROOT)}: {href}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"documentation validated: {len(paths)} canonical documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
