# Tasks

## 1. Python lock

- [x] 1.1 Refresh `uv.lock` with `uv lock --upgrade`; done when OSV reports no advisory in the refreshed lock that a stable release fixes and every `mise run check` command passes on the refreshed environment. `uv lock --upgrade` moves filelock 4.2.7 and patchright 1.64.4 and nothing else. OSV reports only scrapy's PYSEC-2017-83, which has no fixed release, and all nine commands pass, with 89 tests.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass.
