# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The lane's lock at the cutoff
`2026-11-11T15:27:41Z` moved 1 of 150 packages, `impit` 0.15.2 → 0.15.3, and added none.
`crawlee` requires it; no repository source imports it.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow that are at least 24 hours old.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.
- Moving the Python runtime line: Python 3.15 is a separate decision.

## Decisions

### Only the lock moves, by the native release-age option

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes.

### The moved package is a routine release of an existing dependency

`impit` 0.15.3 is a patch release of a package the lock already carries, not yanked, with the same
54 native wheel tags and `requires-python` as 0.15.2. OSV reports no advisory for it.

## Risks / Trade-offs

- [The moved package behaves differently] → The test suite and the behaviour gate run on the
  refreshed lock before landing, and a failure stops the move.
