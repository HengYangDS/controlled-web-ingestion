# Proposal

## Why

The GitHub workflow pins `actions/checkout` v4.2.2, `actions/setup-python` v5.6.0,
`astral-sh/setup-uv` v5.4.0 and `gitleaks/gitleaks-action` v2.3.9. All four target Node 20, which
GitHub has deprecated: hosted runners force them onto Node 24 and annotate every run with a
deprecation warning, as the 18 October 2026 run of the published `dev` shows. The GitHub job also
requests Gitleaks 8.30.0, while the mise configuration and the GitLab image use 8.30.1. `uv.lock`
resolves 74 packages to releases older than their current stable ones.

## What Changes

- Pin `actions/checkout` v7.0.1, `actions/setup-python` v7.0.0, `astral-sh/setup-uv` v10.3.0 and
  `gitleaks/gitleaks-action` v3.0.0 by commit in `.config/ci/pipeline.cue`, all Node 24 releases,
  request Gitleaks 8.30.1 in the GitHub job, and regenerate `.github/workflows/verify.yml`.
- Refresh `uv.lock` with `uv lock --upgrade`: 74 packages move to their current stable release,
  9 are added and 1 is removed. `requires-python` stays `>=3.12`.
- The CI contract tests read the Gitleaks and uv versions from `.config/mise/config.toml` and
  require every action to be pinned by a full commit, instead of repeating each literal pin.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The GitHub workflow keeps its jobs, matrix and commands with new action pins, and the GitLab
pipeline is unchanged. The mise tools and both CI images are already at their current stable
releases and stay as they are. Moving the Python runtime to 3.15 is out of scope. Hosted
acceptance of both pipelines follows the landing. `tasks.md` is the sole progress ledger.
