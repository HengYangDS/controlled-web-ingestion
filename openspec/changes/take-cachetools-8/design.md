# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. `cachetools` reaches the repository only through
`crawlee`, which requires `cachetools>=5.5.0`. A scratch lock at the cutoff `2026-11-07T07:31:00Z`
moved exactly `cachetools` from 7.3.0 to 8.0.0.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow that are at least 24 hours old.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.

## Decisions

### Only the lock moves, by the native release-age option

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes.

### `cachetools 8.0.0` is a major release that `crawlee`'s use does not reach

Its breaking changes drop Python 3.10, the deprecated `@cachedmethod` features and
`@cached(cache=None)`, require `__len__` from custom caches used with `info=True`, make `CacheInfo`
public and change what the decorators return. `crawlee` imports only `LRUCache` and uses a plain
instance as its robots.txt cache; no module of this repository imports `cachetools`. The release
needs Python 3.11 or later, which the repository's 3.12 floor meets, has no dependencies, and OSV
reports no advisory for it; like 7.3.0 it is published without PyPI provenance by the same author.

## Risks / Trade-offs

- [`crawlee`'s robots.txt cache behaves differently] → The test suite and the behavior gate run on
  the refreshed lock before landing, and a failure stops the move and returns the lock to 7.3.0.
