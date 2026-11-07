# Tasks

## 1. Python lock

- [x] 1.1 Refresh `uv.lock` to the newest releases at least 24 hours old with `uv lock --upgrade --exclude-newer` and a plain `uv lock`; done when the lock moves exactly `cachetools`, `crawlee`, `pydantic`, `pydantic-core` and `w3lib` and adds `frostwork`, `uv lock --check` passes, no cutoff option persists, OSV reports no new advisory, and every `mise run check` command passes, including the tests. `uv lock --upgrade --exclude-newer=2026-11-06T13:44:05Z` and a plain `uv lock` moved exactly `cachetools 7.3.0`, `crawlee 1.11.1`, `pydantic 2.14.3`, `pydantic-core 2.50.4` and `w3lib 2.6.0` and added `frostwork 0.2.2`; `uv lock --check` passes and no cutoff option persists; OSV reports only `scrapy 2.19.0`'s PYSEC-2017-83, already present before the move and fixed by no release; all `mise run check` commands pass, including 89 tests.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
