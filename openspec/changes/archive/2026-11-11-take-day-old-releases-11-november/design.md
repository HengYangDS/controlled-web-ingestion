# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The lock at the cutoff `2026-11-10T10:25:01Z`
moved 8 of 149 packages and added `lazy-importer 0.1.0`: `apify-fingerprint-datapoints` 0.16.0,
`crawlee` 1.11.2, `filelock` 4.2.10, `impit` 0.15.2, `importlib-metadata` 10.2.0, `openai` 3.49.0,
`playwright` 1.65.0 and `soupsieve` 4.1, the set the 10 November measurement expected. `pyee` 16,
`snowballstemmer` 3 and `xxhash` 4 stay out: the ranges of the packages that require them exclude
those majors.

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

### The moved packages are routine releases of existing dependencies

Each is a patch or minor release of a package the lock already carries, not yanked, with wheels for
the same CPython versions. OSV reports no advisory for any of them. `playwright` reaches the
repository only through `crawlee[playwright]`; no job or test installs or drives a browser.

### `lazy-importer 0.1.0` is admitted with one condition

- **Need.** `importlib-metadata` 10.2.0 declares it for Python before 3.15. Its release notes
  (#554) call it the backport of PEP 810's lazy imports, which 3.15 provides natively.
- **Identity.** PyPI holds Trusted Publishing attestations for both files, from GitHub
  `pganssle/lazy_importer` (workflow `publish.yml`, environment `release`).
- **Install surface.** One pure `py3-none-any` wheel with no dependencies and no install scripts,
  under Apache-2.0, with no OSV advisory.
- **Condition.** The project is new: the repository was created on 19 October 2026, and 0.1.0 is
  its only release. It changes how modules load, so any import-behaviour failure in the test suite
  or the behaviour gate stops the move and returns the lock to `importlib-metadata` 10.1.0.

## Risks / Trade-offs

- [A moved package behaves differently] → The test suite and the behaviour gate run on the
  refreshed lock before landing, and a failure stops the move.
- [`lazy-importer` defers an import that a test relied on at import time] → The suite runs on
  Python 3.12, 3.13 and 3.14, which all take the backport; a failure stops the move.
