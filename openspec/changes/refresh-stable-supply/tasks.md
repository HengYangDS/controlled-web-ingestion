# Tasks

## 1. Toolchain

- [ ] 1.1 Declare Node 26.12.1, Python 3.14.9, Ruff 0.17.2 and uv 0.13.5 in `.config/mise/config.toml` and relock with `mise lock`; done when `mise.lock` carries checksums for every declared platform and `mise install --locked` succeeds.

## 2. CI supply

- [ ] 2.1 Pin `actions/setup-python` v7.1.0 and `astral-sh/setup-uv` v10.3.2 by commit and the uv 0.13.5 images by index digest in `.config/ci/pipeline.cue`, and regenerate both projections; done when `tools/ci/project.py --check` and the CI contract tests pass.

## 3. Python lock

- [ ] 3.1 Refresh `uv.lock` with `uv lock --upgrade`; done when OSV Scanner reports no advisory in the refreshed lock that a stable release fixes and every `mise run check` command passes on the refreshed environment.

## Workflow follow-up

- Resulting-HEAD proof under the rebound ETHOS runtime, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Publication and hosted acceptance follow separately; this pass stays local.
