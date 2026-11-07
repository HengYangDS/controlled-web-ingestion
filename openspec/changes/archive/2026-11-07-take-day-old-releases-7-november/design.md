# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The previous lock move, `take-day-old-releases`
on 6 November 2026, took six releases. A scratch lock at the cutoff `2026-11-06T13:05:47Z` moved
exactly these five packages and added `frostwork 0.2.2`.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow that are at least 24 hours old.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.
- Taking releases younger than a day, among them `scrapy 2.20.0`, which requires `w3lib 2.6.0`.

## Decisions

### Only the lock moves, by the native release-age option

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes.

### `frostwork` comes in as `w3lib`'s own dependency

`w3lib 2.6.0` requires `frostwork>=0.2.2`. `frostwork` is published by the Scrapy project from
`scrapy/frostwork` with PyPI trusted publishing, under Apache-2.0, as prebuilt wheels for every
platform the repository runs, and it depends only on `typing-extensions`. OSV reports no advisory
for any of the six releases. No module imports `w3lib` or `frostwork` directly; `w3lib` reaches the
repository through `scrapy` and `parsel`.

## Risks / Trade-offs

- [`w3lib 2.6.0` changes how HTML encodings are detected] → It detects a body without a BOM or a
  declaration the way Firefox does, resolves labels by the Encoding Standard, no longer supports
  UTF-32 and reports UTF-8 as `utf-8`. Scrapy decodes responses through it, so the test suite and
  the behavior gate run on the refreshed lock before landing, and any encoding-sensitive failure
  stops the move and returns the lock to the previous versions.
- [`frostwork` is marked beta] → It is pinned only through `w3lib`'s lower bound, and the next
  lock move takes its fixes.
