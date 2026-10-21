# Tasks

## 1. uv release

- [x] 1.1 Require in the CI contract test that the GitHub projection requests the uv version declared in `.config/mise/config.toml`; done when the test fails because the workflow requests none. It failed because the workflow did not request `0.13.1`.
- [x] 1.2 Declare uv 0.13.4 in `.config/mise/config.toml` and relock it with `mise lock`; done when `mise install --locked` provides uv 0.13.4 and the lock differs only in its uv entry. Both hold, and the three locked checksums equal the digests of the release assets.
- [x] 1.3 Name uv 0.13.4 once in `.config/ci/pipeline.cue`, move the three GitLab images to its digest-pinned Debian Trixie images, pass it to setup-uv and regenerate both projections; done when `tools/ci/project.py --check`, the contract tests and every `mise run check` command pass. All pass in the lane on uv 0.13.4.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
