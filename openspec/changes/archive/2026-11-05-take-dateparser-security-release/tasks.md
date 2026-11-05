# Tasks

## 1. Python lock

- [x] 1.1 Refresh `uv.lock` to the newest releases at least 24 hours old with `uv lock --upgrade --exclude-newer` and a plain `uv lock`; done when dateparser resolves to 1.5.0, OSV reports no advisory in the refreshed lock that a stable release fixes, and every `mise run check` command passes. `uv lock --upgrade --exclude-newer=2026-11-04T12:46:17Z` and a plain `uv lock` moved only dateparser 1.4.3 to 1.5.0, persisted no option, and `uv lock --check` passes. OSV reports only scrapy's PYSEC-2017-83, which no release fixes. All nine `mise run check` commands pass, including 89 tests.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
