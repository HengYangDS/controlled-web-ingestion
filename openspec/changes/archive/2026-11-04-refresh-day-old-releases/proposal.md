# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release. Since 4 November 2026 the workstation's lock moves admit only releases that are at least
24 hours old. On 5 November 2026 `uv.lock` resolves `coverage` 7.17.0 and `soupsieve` 3.0.4, while
coverage 7.17.1 and soupsieve 4.0 are the newest releases its ranges allow that have aged a day.
Later releases, such as filelock 4.2.8, platformdirs 4.14.4 and openai 3.45.0, age a day only later
on 5 November and wait for the next move.

## What Changes

- Refresh `uv.lock` with `uv lock --upgrade --exclude-newer=<now minus 24 hours>`, then run a plain
  `uv lock` so that the cutoff is not persisted in the lock. `requires-python` stays `>=3.12`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`uv.lock` only. The pipelines keep their jobs, matrix, commands and pins, and the Firecrawl stack
keeps its reviewed images, so no runtime record is added. `main` follows at the next review batch,
through a pull request on GitHub and a merge request on GitLab. `tasks.md` is the sole progress
ledger.
