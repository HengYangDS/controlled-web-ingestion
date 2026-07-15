#!/usr/bin/env python3
"""Validate the canonical documentation kernel and local Markdown links."""

from __future__ import annotations

import re
import subprocess
import sys
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ("architecture", "decisions", "evidence", "reference", "start", "plans")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
TEXT_SUFFIXES = frozenset(
    {".json", ".jsonl", ".md", ".py", ".sh", ".toml", ".yaml", ".yml"}
)
TEXT_FILENAMES = frozenset(
    {".gitignore", "AGENTS.md", "CHANGELOG.md", "CONTRIBUTING.md", "README.md"}
)
SINGLE_BLANK_LINE_SUFFIXES = frozenset({".md", ".sh", ".toml", ".yaml", ".yml"})
SINGLE_BLANK_LINE_FILENAMES = TEXT_FILENAMES


def tracked_text_paths() -> list[Path]:
    paths = (
        subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .split("\0")
    )
    return [
        ROOT / path
        for path in paths
        if path
        and (Path(path).suffix in TEXT_SUFFIXES or Path(path).name in TEXT_FILENAMES)
    ]


def text_layout_failures(path: Path) -> list[str]:
    relative = path.relative_to(ROOT)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"tracked text is not UTF-8: {relative}"]
    failures: list[str] = []
    if text and not text.endswith("\n"):
        failures.append(f"tracked text lacks final newline: {relative}")
    lines = text.splitlines()
    blank_run = 0
    for number, line in enumerate(lines, start=1):
        if line.rstrip(" \t") != line:
            failures.append(f"trailing whitespace: {relative}:{number}")
        if not line:
            blank_run += 1
            if blank_run == 2 and _requires_single_blank_lines(path):
                failures.append(
                    f"multiple consecutive blank lines outside Python: {relative}:{number - 1}"
                )
            if blank_run == 3:
                failures.append(
                    f"three or more consecutive blank lines: {relative}:{number - 2}"
                )
        else:
            blank_run = 0
    if path.suffix in {".json", ".jsonl"}:
        for number, line in enumerate(lines, start=1):
            if not line:
                failures.append(
                    f"decorative blank line in machine-readable file: {relative}:{number}"
                )
    if path.suffix == ".py":
        failures.extend(_python_module_spacing_failures(path, lines))
    return failures


def _requires_single_blank_lines(path: Path) -> bool:
    return (
        path.suffix in SINGLE_BLANK_LINE_SUFFIXES
        or path.name in SINGLE_BLANK_LINE_FILENAMES
    )


def _python_module_spacing_failures(path: Path, lines: list[str]) -> list[str]:
    top_level_starts = _python_module_definition_starts(path, lines)
    failures: list[str] = []
    for previous, current in zip(top_level_starts, top_level_starts[1:]):
        if not _has_two_blank_lines_before(lines, previous, current):
            relative = path.relative_to(ROOT)
            failures.append(
                f"Python module-level definitions require two blank lines: {relative}:{current}"
            )
    return failures


def _python_module_definition_starts(path: Path, lines: list[str]) -> list[int]:
    try:
        with tokenize.open(path) as source:
            tokens = tokenize.generate_tokens(source.readline)
            indent = 0
            starts: list[int] = []
            for token in tokens:
                if token.type == tokenize.INDENT:
                    indent += 1
                elif token.type == tokenize.DEDENT:
                    indent -= 1
                elif (
                    indent == 0
                    and token.type == tokenize.NAME
                    and token.string in {"class", "def"}
                ):
                    starts.append(_module_definition_start(lines, token.start[0]))
            return starts
    except (SyntaxError, tokenize.TokenError, UnicodeDecodeError):
        return []


def _has_two_blank_lines_before(lines: list[str], previous: int, current: int) -> bool:
    between = lines[previous : current - 1]
    if len(between) >= 2 and not between[-1].strip() and not between[-2].strip():
        return True
    return _is_standalone_main_guard(lines, previous, current)


def _module_definition_start(lines: list[str], definition_line: int) -> int:
    previous_line = definition_line - 2
    while previous_line >= 0 and not lines[previous_line].strip():
        previous_line -= 1
    if previous_line < 0 or not lines[previous_line].lstrip().startswith("@"):
        return definition_line
    while previous_line > 0 and lines[previous_line - 1].lstrip().startswith("@"):
        previous_line -= 1
    return previous_line + 1


def _is_standalone_main_guard(lines: list[str], previous: int, current: int) -> bool:
    intervening = lines[previous - 1 : current - 1]
    return (
        len(intervening) == 7
        and not intervening[2].strip()
        and not intervening[3].strip()
        and intervening[4].strip() == 'if __name__ == "__main__":'
        and intervening[5].strip() == "unittest.main()"
        and not intervening[6].strip()
    )


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
            failures.append(
                f"canonical document lacks complete front matter: {path.relative_to(ROOT)}"
            )
        for href in LINK.findall(path.read_text(encoding="utf-8")):
            target = href.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                failures.append(
                    f"broken local link in {path.relative_to(ROOT)}: {href}"
                )
    for path in tracked_text_paths():
        if path.exists():
            failures.extend(text_layout_failures(path))
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"documentation validated: {len(paths)} canonical documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
