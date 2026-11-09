## Context

See [proposal.md](proposal.md). ETHOS's paradigm keeps one version source, `VERSION`, in a
repository that declares release tags, reads a Keep a Changelog 1.1.0 file with bracketed headings,
and asks for a `LICENSE` grant beside them; a `[project] version` in `pyproject.toml` counts as a
second source. Hatchling reads a dynamic version from a file with `[tool.hatch.version]`, as the
other governed Python repositories already do. ETHOS reads `[release]` of `.ethos/release.toml` only
for `mirror`; its `version_source` and `tag_pattern` keys, kept from the July scaffold, have no
reader.

## Goals / Non-Goals

**Goals:**

- Give the repository one version, `0.1.0`, read from `VERSION` by the package build.
- Grant the MIT License, as every other released governed repository does.
- Keep a Changelog in the shared grammar and declare `v*` release tags.

**Non-Goals:**

- Tagging `v0.1.0` or publishing a Release; that follows in the lane that binds ETHOS
  0.2.0-beta.7.
- Changing any ingestion behaviour, dependency version, CI job or gate.

## Decisions

- `VERSION` holds `0.1.0`, the first version the repository will release; `pyproject.toml` declares
  `dynamic = ["version"]` and reads it through `[tool.hatch.version]`, so no second source remains.
- `CHANGELOG.md` keeps the release's notes under `[Unreleased]` until the release names them
  `[0.1.0]`.
- Drop `version_source` and `tag_pattern` from `[release]`; with `VERSION` as the source they would
  name a false one.
- Refresh `uv.lock` with a plain `uv lock`, which changes only the project's own entry.

## Risks / Trade-offs

- [A tool reads the package version from `pyproject.toml`] → The lock, the build and every check run
  in the lane; a reader of the static field would fail there.
- [A license grant is hard to withdraw for published versions] → The owner chose the MIT License on
  9 November 2026.

## Migration Plan

Add the files, refresh the lock, run every check, prove the archived head, land, publish `dev`, take
`main` through the pull request and merge request, and resynchronize the original developer
environment, whose editable project then reports 0.1.0. To roll back, revert the lane's commits.
