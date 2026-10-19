# Tasks

## 1. CI supply

- [ ] 1.1 Pin `actions/checkout` v7.0.1, `actions/setup-python` v7.0.0, `astral-sh/setup-uv` v10.3.0 and `gitleaks/gitleaks-action` v3.0.0 by commit and request Gitleaks 8.30.1 in `.config/ci/pipeline.cue`, regenerate the GitHub workflow, and make the CI contract tests read the mise declaration; done when `tools/ci/project.py --check` and the contract tests pass.

## 2. Python lock

- [ ] 2.1 Refresh `uv.lock` with `uv lock --upgrade`; done when every `mise run check` command passes on the refreshed environment.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
