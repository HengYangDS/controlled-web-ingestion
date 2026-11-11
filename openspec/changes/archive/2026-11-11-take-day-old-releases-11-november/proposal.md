# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old. At the
cutoff `2026-11-10T10:25:01Z`, 8 newer releases fall within `uv.lock`'s ranges. One of them,
`importlib-metadata 10.2.0`, adds a dependency, `lazy-importer 0.1.0`.

## What Changes

- Refresh `uv.lock` with `uv lock --upgrade --exclude-newer=<cutoff>`, then run a plain `uv lock` so
  that the cutoff is not persisted in the lock. `requires-python` stays `>=3.12`.
- Admit one new transitive package, `lazy-importer 0.1.0`, which `importlib-metadata 10.2.0`
  requires on Python before 3.15.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`uv.lock` only. The pipelines keep their jobs, matrix, commands and pins. `main` follows through a
pull request on GitHub and a merge request on GitLab. `tasks.md` is the sole progress ledger.
