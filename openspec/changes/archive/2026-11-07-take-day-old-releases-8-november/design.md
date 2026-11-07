# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`. The previous lock move,
`take-day-old-releases-7-november`, took five releases and brought `frostwork`. A scratch lock at
the cutoff `2026-11-06T20:00:00Z` moved exactly these four packages, added `aiodns 4.0.4`, `aioftp
0.28.3`, `formerly 0.1.0` and `pycares 5.2.1`, and removed `brotlicffi` and `pypydispatcher`. Mise
declares `ruff` for the format and lint checks.

## Goals / Non-Goals

**Goals:**

- Move the Python lock to the newest releases its ranges allow that are at least 24 hours old.
- Move Mise's `ruff` to 0.17.4.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.
- Changing the Mise lockfile format; no step runs `mise lock --upgrade`.

## Decisions

### Only the locks move, by native commands

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes. `mise lock` relocks `ruff` in place and keeps `lockfile_version =
3`.

### Scrapy's new dependencies come in as its own

`scrapy 2.20.0` requires `aiodns`, `aioftp` and `formerly`, and `aiodns` requires `pycares`.
`formerly` is published by the Scrapy project from `scrapy/formerly`; `aiodns` and `aioftp` come
from the aio-libs organization; each of the three publishes with PyPI trusted publishing, and
`pycares`, like its earlier releases, without provenance. `pycares` ships prebuilt wheels for
CPython 3.12 to 3.14 on macOS arm64 and Linux aarch64 and x64, so no source build is needed. Their
licenses are MIT, Apache-2.0 and BSD-3-Clause. OSV reports no advisory for any moved or added
release; `scrapy 2.20.0` still carries `PYSEC-2017-83`, which `2.19.0` carries too and no release
fixes. `brotlicffi` and `pypydispatcher` were PyPy-only dependencies of `scrapy 2.19.0`. No module
imports any of these packages directly.

## Risks / Trade-offs

- [`scrapy 2.20.0` detects encodings, base URLs and meta refresh like a browser, through
  `frostwork`, and deprecates non-asyncio Twisted reactors] → The repository's only Scrapy path
  is the framework comparison's spider, which sets no reactor. The test suite and the behavior gate
  run on the refreshed lock before landing, and any encoding-sensitive failure stops the move and
  returns the lock to the previous versions.
- [`ruff` 0.17.4 changes a check result] → Its stable rules are unchanged; the format and lint
  checks run on the moved lock before landing.
