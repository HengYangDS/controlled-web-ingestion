# Tasks

## 1. GitHub triggers

- [x] 1.1 Require in the CI contract test that the GitHub projection triggers on pushes to `dev`, `main` and `proposal/**` and on pull requests to `dev` and `main`, and names no `candidate/` branch; done when the test fails on the current projection. It failed on the `main` and `candidate/**` triggers.
- [x] 1.2 Set those triggers in `.config/ci/pipeline.cue` and regenerate `.github/workflows/verify.yml`; done when `tools/ci/project.py --check`, the contract tests and every `mise run check` command pass. All pass, with 88 tests.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass.
