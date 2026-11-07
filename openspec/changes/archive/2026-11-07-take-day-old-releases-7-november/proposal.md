# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old. By the
evening of 7 November 2026 five newer releases in `uv.lock`'s ranges have aged a day: `cachetools
7.3.0`, `crawlee 1.11.1`, `pydantic 2.14.3`, `pydantic-core 2.50.4` and `w3lib 2.6.0`. `w3lib 2.6.0`
brings one new dependency, `frostwork 0.2.2`.

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
