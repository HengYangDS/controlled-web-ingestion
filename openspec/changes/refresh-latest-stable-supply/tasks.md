# Tasks

## 1. Toolchain

- [x] 1.1 Declare Node 26.13.0, Python 3.14.10, Ruff 0.17.3 and uv 0.13.6 in `.config/mise/config.toml` and lock it again with `mise lock`; done when `mise.lock` carries checksums for every declared platform and `mise install --locked` succeeds. `mise lock` checked 24 targets and pruned the four superseded versions, and `mise install --locked` succeeds.

## 2. CI supply

- [x] 2.1 Pin `astral-sh/setup-uv` v10.3.3 by commit and the uv 0.13.6 images by index digest in `.config/ci/pipeline.cue`, and regenerate both projections; done when `tools/ci/project.py --check` and the CI contract tests pass. Both pass, within the 88 tests.

## 3. Python lock

- [x] 3.1 Refresh `uv.lock` with `uv lock --upgrade`; done when OSV reports no advisory in the refreshed lock that a stable release fixes and every `mise run check` command passes on the refreshed environment. OSV reports only scrapy's PYSEC-2017-83, which has no fixed release, and all nine commands pass.

## 4. Firecrawl Redis

- [x] 4.1 Record the `redis:8.10.3-alpine` index digest in `system/supply-chain/firecrawl-provenance.json` and pin it in `system/projections/firecrawl-isolated-compose.yaml`; done when the runtime unit test that compares both files passes, and `docker compose pull --policy always` returns the recorded identity, which `web-ingest` accepts. The pull returned the recorded identity on linux/arm64, and the validation run accepted all five images.
- [x] 4.2 Run `web-ingest validate-workloads` against the moved set; done when its evidence record is committed under `evidence/verification/` and no project resource remains. The run wrote `2026-10-31-controlled-web-ingestion-runtime-validation.json` and left no container, volume, network or listener.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
