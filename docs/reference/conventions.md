---
subject: controlled-web-ingestion:repository-conventions
role: reference
state: active
relations:
  canonical_for: repository text layout and formatting boundaries
  enforced_by: tools/ci/check_documentation.py
---

# Repository Conventions

## Text layout

All tracked text is UTF-8, LF-terminated, has a final newline, and has no
trailing whitespace. `.editorconfig` is the editor-facing baseline; the
repository-owned documentation check is the enforceable acceptance gate.

## Blank lines

Blank lines express structure; they do not decorate it.

- **One blank line** separates adjacent semantic units within the same level:
  Markdown paragraphs, lists, tables, code fences, YAML mapping blocks, TOML
  tables, shell command blocks, and Python definitions within one module.
- **Two blank lines** separate Python module-level definitions, as required by
  PEP 8. A standalone `if __name__ == "__main__"` guard may sit between
  definition groups without changing that boundary. Canonical Markdown uses
  headings plus one blank line instead.
- **No empty separator** is used inside a compact machine-readable collection
  unless its format requires it. JSON and JSONL never use decorative blank
  lines. YAML and TOML use one blank line only to separate logical blocks.
- **Three or more consecutive blank lines** are never valid in tracked text.

The boundary is semantic, not cosmetic: a formatter may normalize whitespace,
but it must not rewrite evidence values, serialized JSON, shell heredocs, or
Markdown code examples.

## Source-language rules

Python follows PEP 8: two blank lines between module-level definitions, one
blank line between methods, and no blank line that splits a coherent statement
block. Shell keeps one blank line between logical command groups. Generated
outputs belong under their declared generated-artifact paths rather than being
formatted or manually curated in place.

## Configuration rules

TOML and YAML use one blank line between top-level tables, mappings, or jobs;
related keys stay contiguous. A comment belongs to the block it explains, with
no decorative blank line separating it from that block. CI projections remain
thin and place their owner-command sequence in one contiguous command block.

## Documentation rules

Canonical Markdown starts with complete front matter, then one blank line,
then the title. Use one blank line around headings, paragraphs, lists, tables,
and fenced code blocks. Do not insert empty paragraphs merely to create visual
space. The result must remain readable in raw text and stable under review.

## Formatters

The ETHOS repository paradigm binds one formatter per text carrier class, each
configured under `.config/checks/<tool>/` and run from the host installation:

- Prettier formats Markdown and YAML at 100 columns with preserved prose
  wrapping and leaves embedded code examples untouched.
- taplo formats TOML at 100 columns.
- Ruff formats Python at 100 columns for Python 3.12 and later.

Immutable records keep their captured bytes and are not formatter inputs:
archived OpenSpec Changes, `evidence/`, `docs/evidence/chronicle/`,
`docs/history/` and `docs/plans/`. `.gitattributes` marks the same records,
apart from the archived Changes that ETHOS already keeps, `linguist-vendored`,
so the ETHOS paradigm treats them as received and leaves their layout and
names as captured. The ETHOS skill projections under `.agents/`
follow their packages. JSON is not formatted.

Each proof gate runs the check form from the repository root:

```bash
prettier --config .config/checks/prettier/prettier.toml --ignore-path .gitignore --ignore-path .config/checks/prettier/prettierignore --check '**/*.{md,yaml,yml}'
taplo fmt --config .config/checks/taplo/taplo.toml --check
ruff format --config .config/checks/ruff/ruff.toml --no-cache --check .
```

To fix the same inputs, replace Prettier's `--check` with `--write` and drop
`--check` from the taplo and Ruff commands.
