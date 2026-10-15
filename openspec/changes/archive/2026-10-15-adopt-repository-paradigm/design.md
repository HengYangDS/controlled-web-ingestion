## Context

See proposal.md for motivation. This repository's proof gates run its own
commands through uv, plus the host's `gitleaks` for the security gate. Hosted
CI runs the same uv commands on Python-only images. `docs/reference/conventions.md`
owns the repository's text layout and formatting boundaries, and states that
formatting must not rewrite evidence values, serialized JSON or Markdown code
examples. `docs/evidence/README.md` keeps historical records unrewritten.

## Goals and Non-goals

Goals: close every paradigm gap that does not rename a role branch, and pass the
full proof under the current ETHOS runtime.

Non-goals: changing ingestion behavior, adding a Node toolchain, formatting
JSON, moving formatter checks into hosted CI before ETHOS settles the shared
toolchain verbs, and renaming any branch before ETHOS can migrate role branches
natively.

## Decisions

- The three formatters run from the host's Homebrew installation, as `gitleaks`
  already does. Each has one proof gate with the security gate's shape, so the
  proof records each formatter separately.
- Prettier formats Markdown and YAML only, with embedded code formatting off so
  Markdown code examples keep their bytes. Its ignore file adds, to
  `.gitignore`, the immutable records (`openspec/changes/archive/`,
  `evidence/`, `docs/evidence/chronicle/`, `docs/history/`, `docs/plans/`) and
  the ETHOS skill projections under `.agents/`.
- taplo checks the authored TOML; its configuration excludes the archive,
  `evidence/`, `.agents/`, `build/` and `.venv/`, with patterns resolved from the
  repository root. Ruff checks only `*.py` and `*.pyi`, because its default
  inclusion also formats Python examples inside Markdown, and runs without a
  cache, because the root `.ruff_cache/` is denied residue here.
- `docs/reference/conventions.md` records the bindings and the check and fix
  commands.
- The peer remote becomes `gitlab` in `.ethos/release.toml`, and
  `git remote rename origin gitlab` renames the local remote in the same batch.
  The user directed this rename for every ETHOS-managed repository on
  2026-10-14.
- `[commit_policy]` keeps its signing settings and drops `subject_pattern`;
  ETHOS derives the common grammar, which also admits the `!` breaking marker.
- The role table, `tests/contract/test_ethos_boundary.py` and the current
  branch names in `docs/decisions/dr-0002-delivery-train-boundary.md` and
  `docs/start/adopter-governance.md` change together in one later commit. ETHOS
  has no admitted path that renames the accepted and candidate refs; committing
  standard names first would point the committed policy at refs that do not
  exist.

## Risks and Trade-offs

- [A formatter rewrites a protected record] → ignore and exclude lists are
  checked against the tracked roots, and every excluded file is byte-identical
  after formatting.
- [Host formatter versions drift] → the gates record each tool's output; the
  shared toolchain decision stays with ETHOS.
- [The remote rename breaks a consumer that names `origin`] → the release
  binding, branch tracking and remote-tracking refs move together, and the proof
  runs after the rename.
