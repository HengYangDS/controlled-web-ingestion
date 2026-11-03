# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The Firecrawl stack's images are pinned by
digest in `system/supply-chain/firecrawl-provenance.json` and moved with `refresh-locked-supply` on
2 November 2026; no image has moved since. On 3 November 2026 the newest releases were read from
PyPI, Mise, the GitHub releases API, Docker Hub and GHCR.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.
- Adopting Python 3.15 for the Mise runtime or the CI matrix.

## Decisions

### Only the lock moves

The audit found the lock behind on two patch releases and everything else current. Neither package
is part of the isolated Firecrawl stack, and the static transport does not import them, so the
repository's lock contract applies: OSV reads the refreshed lock, and every `mise run check` command
runs on the refreshed environment. The runtime acceptance that an image move requires does not run.

### Upstream ranges and wheels still hold some rows

`pyee` 14.0.0, `snowballstemmer` 2.2.0 and `xxhash` 3.8.2 stay below their newest major releases
because `playwright`, `patchright` and `crawl4ai` refuse those releases. Python 3.15.2 stays out of
the Mise runtime because `fastuuid` 0.14.0 and `pyyaml` 6.0.3 publish no CPython 3.15 wheel.

## Risks / Trade-offs

- [A patch release changes behavior the benchmark relies on] → Every `mise run check` command runs
  on the refreshed environment before proof, and the hosted matrix runs on 3.12, 3.13 and 3.14.
