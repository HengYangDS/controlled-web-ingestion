# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old. The
evening measurement of 12 November found one newer release within `uv.lock`'s ranges: `impit
0.15.3`.

## What Changes

- Refresh `uv.lock` with `uv lock --upgrade --exclude-newer=<cutoff>`, then run a plain `uv lock` so
  that the cutoff is not persisted in the lock. `requires-python` stays `>=3.12`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`uv.lock` only. The pipelines keep their jobs, matrix, commands and pins. `main` follows through a
pull request on GitHub and a merge request on GitLab. `tasks.md` is the sole progress ledger.
