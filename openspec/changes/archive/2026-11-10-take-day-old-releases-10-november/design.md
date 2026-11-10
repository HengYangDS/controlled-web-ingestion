# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. `regex` reaches the repository only through
`dateparser`, `nltk` and `tiktoken`. A scratch lock at the cutoff `2026-11-09T03:52:47Z` moved
exactly `regex` from 2026.11.7 to 2026.11.9 and added or removed no package.

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

### `regex 2026.11.9` is a routine release of a transitive dependency

It is published with wheels for the same CPython versions as 2026.11.7, 3.11 to 3.15, so no
supported platform builds it from source. It is not yanked, and OSV reports no advisory for it.

## Risks / Trade-offs

- [A pattern used by `dateparser`, `nltk` or `tiktoken` behaves differently] → The test suite and
  the behavior gate run on the refreshed lock before landing, and a failure stops the move and
  returns the lock to 2026.11.7.
