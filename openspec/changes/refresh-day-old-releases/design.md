# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The previous lock move, `take-uv-rustls-fix` on
3 November 2026, moved uv to 0.13.7. On 5 November 2026 a scratch copy measured what a lock that
admits only day-old releases would move: `coverage` and `soupsieve`, nothing else.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow that are at least 24 hours old.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.
- Publishing `main`; it follows at the next review batch.

## Decisions

### Only the lock moves, by the native release-age option

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes.

### soupsieve 4.0 is a major release

soupsieve reaches this repository only through `beautifulsoup4` 4.15.0, which `crawl4ai` 0.9.5
requires, and no source module imports either. soupsieve 4.0 requires Python 3.11.5 or newer, which
the declared `>=3.12` satisfies. `coverage` reaches it only through `pytest-cov`. Every `mise run
check` command runs on the refreshed environment, and the hosted matrix runs on 3.12, 3.13 and 3.14.

## Risks / Trade-offs

- [A major release changes behavior that crawl4ai's HTML parsing relies on] → The tests and the
  hosted matrix run on the refreshed lock before landing, and the lock returns to soupsieve 3.0.4 if
  either fails.
