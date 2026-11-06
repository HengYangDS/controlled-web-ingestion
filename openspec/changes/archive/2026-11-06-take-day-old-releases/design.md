# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The previous lock move,
`take-dateparser-security-release` on 5 November 2026, took dateparser 1.5.0. A scratch lock at the
cutoff `2026-11-05T01:00:00Z` moved exactly these six packages and no other.

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

### All six packages are indirect dependencies

No source, tool or test module imports any of them. coverage reaches the repository through
`pytest-cov` in the development group, filelock through `huggingface-hub` and `tldextract`, openai
through `unclecode-litellm` and `crawl4ai`, platformdirs through `scrapy`, soupsieve through
`beautifulsoup4` and `crawl4ai`, and typing-inspection through `pydantic`. Every `mise run check`
command runs on the refreshed environment, and the hosted matrix runs on 3.12, 3.13 and 3.14.

## Risks / Trade-offs

- [A release changes a behavior that a dependent relies on] → The tests and the hosted matrix run
  on the refreshed lock before landing, and the lock returns to the previous versions if either
  fails.
