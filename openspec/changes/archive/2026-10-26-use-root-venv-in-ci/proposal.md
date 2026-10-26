# Proposal

## Why

The generated-artifact topology of the bound ETHOS runtime retires `build/runtime/venv`. Its
producer entrypoint audit reports every CI or tool entrypoint that still names that home
(`retired-venv-runtime`), because active execution uses the checkout's single root `.venv` and only
tool caches belong under `build/runtime/tool-cache/`. Both pipelines here still point
`UV_PROJECT_ENVIRONMENT` at `build/runtime/venv/python-<version>`: the GitHub job through
`_githubUv` and the GitLab jobs through `.python-contracts` in `.config/ci/pipeline.cue`. Local
commands already run in the root `.venv`, so CI is the only place that uses the retired home.

## What Changes

- Remove `UV_PROJECT_ENVIRONMENT` from `_githubUv` and `.python-contracts` in
  `.config/ci/pipeline.cue`, so uv uses its default project environment, the root `.venv`, and
  regenerate `.github/workflows/verify.yml` and `.gitlab-ci.yml`.
- Require in the CI contract test that neither projection sets `UV_PROJECT_ENVIRONMENT`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

Both pipelines keep their jobs, matrix, commands, caches and pins. Each Python version still runs in
its own GitHub job and its own GitLab job, so each job's root `.venv` replaces its per-version
directory. Hosted acceptance of both pipelines follows publication. `tasks.md` is the sole progress
ledger.
