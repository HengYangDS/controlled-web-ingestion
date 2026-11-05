# Tasks

## 1. Python lock

- [x] 1.1 Refresh `uv.lock` to the newest releases at least 24 hours old with `uv lock --upgrade --exclude-newer` and a plain `uv lock`; done when OSV reports no advisory in the refreshed lock that a stable release fixes and every `mise run check` command passes. `uv lock --upgrade --exclude-newer=2026-11-04T05:07:06Z` and a plain `uv lock` moved only openai 3.42.1 → 3.45.0, `uv lock --check` passes and no cutoff option persists; OSV reports only scrapy 2.19.0's PYSEC-2017-83, which no release fixes; all nine `mise run check` commands pass, including 89 tests.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows at the next review batch.
