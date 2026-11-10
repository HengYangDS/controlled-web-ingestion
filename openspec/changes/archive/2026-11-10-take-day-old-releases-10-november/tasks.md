# Tasks

## 1. Python lock

- [x] 1.1 Refresh `uv.lock` to the newest releases at least 24 hours old with
      `uv lock --upgrade --exclude-newer` and a plain `uv lock`; done when the lock moves exactly
      `regex` to 2026.11.9, `uv lock --check` passes, OSV reports no advisory beyond the base
      lock's, and every `mise run check` command passes. At the cutoff `2026-11-09T03:52:47Z` the
      lock moved exactly `regex` from 2026.11.7 to 2026.11.9; `uv lock --check` passes and no cutoff
      persists; OSV reports only `scrapy 2.20.0`'s `PYSEC-2017-83`, which the base lock carries and
      no release fixes; all `mise run check` commands pass, 89 tests included.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and
  OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by
  itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge
  request.
