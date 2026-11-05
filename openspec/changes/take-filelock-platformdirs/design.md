# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The previous lock move, `take-day-old-openai` on
5 November 2026, took openai 3.45.0. The release-age reads of 4 November named filelock 4.2.8 and
platformdirs 4.14.4 as the remaining day-old moves for the afternoon of 5 November.

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

### Both packages are indirect dependencies

filelock reaches this repository through `huggingface-hub` and `tldextract`, and platformdirs
through `scrapy`; no source or tool module imports either. Every `mise run check` command runs on
the refreshed environment, and the hosted matrix runs on 3.12, 3.13 and 3.14.

## Risks / Trade-offs

- [A patch release changes a lock or cache path behavior that a dependent relies on] → The tests
  and the hosted matrix run on the refreshed lock before landing, and the lock returns to the
  previous versions if either fails.
