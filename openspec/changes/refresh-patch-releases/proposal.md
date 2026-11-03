# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release. On 3 November 2026 `uv.lock` resolves `filelock` 4.2.6 and `patchright` 1.64.3, while
filelock 4.2.7 and patchright 1.64.4 are the newest releases its ranges allow. The Mise tools, the
pinned actions, the uv images and the Firecrawl images are current.

## What Changes

- Refresh `uv.lock` with `uv lock --upgrade`. `requires-python` stays `>=3.12`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`uv.lock` only. The pipelines keep their jobs, matrix, commands and pins, and the Firecrawl stack
keeps its reviewed images, so no runtime record is added. The design explains what stays.
`tasks.md` is the sole progress ledger.
