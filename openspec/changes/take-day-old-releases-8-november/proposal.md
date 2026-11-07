# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old. By the
morning of 8 November 2026 four newer releases in `uv.lock`'s ranges have aged a day: `click
8.5.1`, `jiter 0.19.0`, `regex 2026.11.7` and `scrapy 2.20.0`. Mise's `ruff` 0.17.4, released on
5 November 2026, is also newer than the declared 0.17.3.

## What Changes

- Refresh `uv.lock` with `uv lock --upgrade --exclude-newer=<now minus 24 hours>`, then run a plain
  `uv lock` so that the cutoff is not persisted in the lock. `requires-python` stays `>=3.12`.
- Declare `ruff` 0.17.4 in `.config/mise/config.toml` and lock it with native `mise lock`, which
  keeps the lockfile at version 3.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`uv.lock`, `.config/mise/config.toml` and `.config/mise/mise.lock`. The pipelines keep their jobs,
matrix, commands and pins. `main` follows through a pull request on GitHub and a merge request on
GitLab. `tasks.md` is the sole progress ledger.
