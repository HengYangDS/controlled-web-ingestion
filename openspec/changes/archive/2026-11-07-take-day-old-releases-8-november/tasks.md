# Tasks

## 1. Python lock

- [x] 1.1 Refresh `uv.lock` to the newest releases at least 24 hours old with `uv lock --upgrade --exclude-newer` and a plain `uv lock`; done when the lock moves exactly `click`, `jiter`, `regex` and `scrapy`, adds exactly `aiodns`, `aioftp`, `formerly` and `pycares`, removes exactly `brotlicffi` and `pypydispatcher`, `uv lock --check` passes, OSV reports no advisory beyond the base lock's, and every `mise run check` command passes. At the cutoff `2026-11-06T20:02:08Z` the lock moved exactly these four packages, added the four and removed the two; `uv lock --check` passes and no cutoff persists; OSV reports only `scrapy 2.20.0`'s `PYSEC-2017-83`, which the base lock's `2.19.0` carries and no release fixes; all `mise run check` commands pass, 89 tests included.

## 2. Mise tools

- [x] 2.1 Declare `ruff` 0.17.4 and lock it with `mise lock`; done when the lock moves only `ruff`, keeps `lockfile_version = 3` with `github-attestations` on each platform, and the format and lint checks pass. `mise lock` checked 24 targets and pruned only `ruff@0.17.3`; the lock diff is the `ruff` block only (11 lines), `lockfile_version` stays 3, and each of the three platform checksums equals the release's asset digest with `github-attestations`; the format and lint checks pass with `ruff` 0.17.4.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
