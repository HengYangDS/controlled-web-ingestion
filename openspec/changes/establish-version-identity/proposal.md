## Why

The owner requires every ETHOS-governed repository to carry a version. This repository has none:
`pyproject.toml` declares `0.0.0`, no `VERSION` or release tag exists, there is no `LICENSE`, and
`CHANGELOG.md` holds one unbracketed scaffold line from July 2026. Its GitHub peer is declared as
public distribution.

## What Changes

- Add `VERSION` with `0.1.0` as the only version source, and read the package version from it
  (`dynamic = ["version"]` with Hatchling's version source), as the other governed Python
  repositories do.
- Add `LICENSE` with the MIT License, as every other released governed repository uses.
- Rewrite `CHANGELOG.md` to Keep a Changelog 1.1.0, whose `[Unreleased]` section summarizes what
  0.1.0 will release.
- Declare release tags in `.ethos/release.toml` as `[protected_refs] tags = ["v*"]`, and drop the
  `version_source` and `tag_pattern` keys of `[release]`, which no reader consults.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`VERSION`, `LICENSE`, `CHANGELOG.md`, `pyproject.toml`, `uv.lock` (the project's own version line)
and `.ethos/release.toml`. The `v0.1.0` tag and its Releases follow in the lane that binds ETHOS
0.2.0-beta.7, as the owner decided on 9 November 2026. `tasks.md` is the sole progress ledger.
