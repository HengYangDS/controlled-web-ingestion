# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The previous lock move,
`refresh-day-old-releases` on 5 November 2026, took coverage 7.17.1 and soupsieve 4.0. A scratch
copy at 13:05 CST measured what a lock that admits only day-old releases would move now: openai
alone.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow that are at least 24 hours old.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.
- Publishing `main`; it follows at the next review batch, together with the next day-old move.

## Decisions

### Only the lock moves, by the native release-age option

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes.

### openai is an indirect dependency

openai reaches this repository only through `unclecode-litellm`, which `crawl4ai` requires, and no
source or tool module imports it. Every `mise run check` command runs on the refreshed environment,
and the hosted matrix runs on 3.12, 3.13 and 3.14.

## Risks / Trade-offs

- [A minor release changes a client behavior that crawl4ai's model calls rely on] → The tests and
  the hosted matrix run on the refreshed lock before landing, and the lock returns to openai 3.42.1
  if either fails.
