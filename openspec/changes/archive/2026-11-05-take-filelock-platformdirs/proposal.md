# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release, and the workstation's lock moves admit only releases that are at least 24 hours old.
platformdirs 4.14.4 ages a day at 15:38 CST and filelock 4.2.8 at 15:46 CST on 5 November 2026,
while `uv.lock` resolves platformdirs 4.14.3 and filelock 4.2.7. With them, every locked release is
the newest that its range allows and that has aged a day.

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
keeps its reviewed images, so no runtime record is added. `main` follows in one review batch with
the earlier day-old moves, through a pull request on GitHub and a merge request on GitLab.
`tasks.md` is the sole progress ledger.
