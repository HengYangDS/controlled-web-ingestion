# Tasks

## 1. Toolchain

- [x] 1.1 Declare uv 0.13.7 in `.config/mise/config.toml` and lock it again with `mise lock`; done when `mise.lock` carries 0.13.7 for every declared platform and no 0.13.6 entry, and `mise install --locked` succeeds. `mise lock` checked 24 targets and pruned only `uv@0.13.6`; the lock holds uv 0.13.7 for linux-arm64, linux-x64 and macos-arm64, each with GitHub attestation provenance, and `mise install --locked uv` succeeds.

## 2. CI supply

- [x] 2.1 Set `_uv` to 0.13.7 and pin the uv 0.13.7 images by index digest in `.config/ci/pipeline.cue`, and regenerate both projections; done when `tools/ci/project.py --check` and the CI contract tests pass. Both pass, within the 89 tests.

## 3. Verification

- [x] 3.1 Run every `mise run check` command with the locked uv 0.13.7; done when all pass and `uv lock --check` reports the lock current. All nine commands pass, and `uv lock --check` resolves the unchanged 147-package lock.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass.
