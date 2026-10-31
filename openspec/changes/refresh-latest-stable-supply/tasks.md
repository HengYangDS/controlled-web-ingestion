# Tasks

## 1. Toolchain

- [ ] 1.1 Declare Node 26.13.0, Python 3.14.10, Ruff 0.17.3, uv 0.13.6 and the Mise floor 2026.10.24 in `.config/mise/config.toml` and lock it again with `mise lock`; done when `mise.lock` carries checksums for every declared platform and `mise install --locked` succeeds.

## 2. CI supply

- [ ] 2.1 Pin `astral-sh/setup-uv` v10.3.3 by commit and the uv 0.13.6 images by index digest in `.config/ci/pipeline.cue`, and regenerate both projections; done when `tools/ci/project.py --check` and the CI contract tests pass.

## 3. Python lock

- [ ] 3.1 Refresh `uv.lock` with `uv lock --upgrade`; done when OSV reports no advisory in the refreshed lock that a stable release fixes and every `mise run check` command passes on the refreshed environment.

## 4. Firecrawl Redis

- [ ] 4.1 Record the `redis:8.10.3-alpine` index digest in `system/supply-chain/firecrawl-provenance.json` and pin it in `system/projections/firecrawl-isolated-compose.yaml`; done when the runtime unit test that compares both files passes, and `docker compose pull --policy always` returns the recorded identity, which `web-ingest` accepts.
- [ ] 4.2 Run `web-ingest validate-workloads` against the moved set; done when its evidence record is committed under `evidence/verification/` and no project resource remains.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
