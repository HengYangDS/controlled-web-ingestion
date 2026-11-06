# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old. By
08:56 CST on 6 November 2026 six newer releases in `uv.lock`'s ranges have aged a day: coverage
7.17.2, filelock 4.2.9, openai 3.46.0, platformdirs 4.14.5, soupsieve 4.0.1 and typing-inspection
0.4.5. With them, every locked release is the newest that its range allows and that has aged a day.

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
keeps its reviewed images, so no runtime record is added. `main` follows through a pull request on
GitHub and a merge request on GitLab. `tasks.md` is the sole progress ledger.
