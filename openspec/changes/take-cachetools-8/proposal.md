# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old. By the
afternoon of 8 November 2026 `cachetools 8.0.0`, released on 7 November 2026, has aged a day. It is
the only newer release in `uv.lock`'s ranges at that cutoff.

## What Changes

- Refresh `uv.lock` with `uv lock --upgrade --exclude-newer=<now minus 24 hours>`, then run a plain
  `uv lock` so that the cutoff is not persisted in the lock. `requires-python` stays `>=3.12`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`uv.lock` only. The pipelines keep their jobs, matrix, commands and pins. `main` follows through a
pull request on GitHub and a merge request on GitLab. `tasks.md` is the sole progress ledger.
