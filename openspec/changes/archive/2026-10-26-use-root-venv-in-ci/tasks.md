# Tasks

## 1. CI environment

- [x] 1.1 Require in the CI contract test that neither projection sets `UV_PROJECT_ENVIRONMENT`; done when the test fails on the current projections. Both contract tests failed on the variable.
- [x] 1.2 Remove `UV_PROJECT_ENVIRONMENT` from `_githubUv` and `.python-contracts` in `.config/ci/pipeline.cue` and regenerate both projections; done when `tools/ci/project.py --check`, the contract tests and every `mise run check` command pass, and no CI or tool entrypoint names `build/runtime/venv`. All pass, and the ETHOS generated-artifact entrypoint audit reports no retired runtime home.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
