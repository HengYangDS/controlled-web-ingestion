# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old. At
13:05 CST on 5 November 2026 openai 3.45.0 has aged a day, and `uv.lock` still resolves openai
3.42.1. Every other locked release is the newest that its range allows and that has aged a day.
filelock 4.2.8 and platformdirs 4.14.4 age a day at about 15:40 CST and wait for the next move.

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
