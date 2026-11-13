# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. At a 24-hour floor on 13 November 2026 the only
newer release within those ranges is `playwright` 1.65.1, a patch release of a package the lock
already carries through `crawlee[playwright]`.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow that are at least 24 hours old.

**Non-Goals:**

- Moving the Mise-declared tools: Prettier 3.10.1, uv 0.13.8 and Ruff 0.17.5 become a day old later
  and move together in the next supply lane.
- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.

## Decisions

### Only the lock moves, by the native release-age option

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes.

## Risks / Trade-offs

- [The patch release changes a browser-backed acquisition] → Every `mise run check` command runs on
  the new lock before the commit, and the hosted pipelines run on both forges before `main` moves;
  reverting the lock rolls it back.
