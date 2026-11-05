# Proposal

## Why

dateparser 1.5.0, published on 4 November 2026 at 12:42 UTC, fixes six regular-expression denial of
service issues that its release notes name: GHSA-rx9v-94ff-9cc2, GHSA-g8fh-jxm9-6qfx,
GHSA-q7fp-xwcm-6x9f, GHSA-gqj4-wf6c-wmcg, GHSA-fmxc-97cw-ph6p and GHSA-jxmm-w6rw-32ch. OSV listed
none of them for 1.4.3 on 5 November. dateparser reaches this repository through `htmldate` and
`trafilatura`, which read dates from fetched pages, so its input is untrusted. The owner's direction
of 2 November 2026 is that every supply chain moves to its latest stable release, and the
workstation's lock moves admit only releases that are at least 24 hours old. dateparser 1.5.0 ages a
day at 20:43 CST on 5 November 2026.

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
