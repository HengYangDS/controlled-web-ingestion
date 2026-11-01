# Proposal

## Why

The GitHub workflow still triggers on the branch roles this repository used before it adopted the
ETHOS repository paradigm on 2026-10-15: pushes to `main` and `candidate/**`, and pull requests to
`main`. Since then ETHOS publishes the accepted branch `dev` and proposals under `proposal/`.
`candidate/dev` stays local, and `main` is an independent release branch that has not moved since
2026-10-15. So none of the ten moves of `dev` on GitHub from 2026-10-15 to 2026-10-31 started a run.
Six got a manual dispatch and four got no GitHub run at all, while GitLab, whose workflow rules
accept any push, ran every one. The delivery-governance requirement that both hosted planes run
their independent jobs for a published head holds only through that manual step.

## What Changes

- Trigger the GitHub workflow on pushes to `dev`, `main` and `proposal/**`, and on pull requests to
  `dev` and `main`, in `.config/ci/pipeline.cue`, and regenerate `.github/workflows/verify.yml`.
- Require in the CI contract test that the GitHub projection triggers on exactly those roles and
  names no `candidate/` branch.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The change restores the existing delivery-governance requirement that both hosted planes run
their jobs for a published head. Ingestion behavior and its contracts are unchanged, so
`.openspec.yaml` sets `skip_specs: true`.

## Impact

Jobs, matrix, commands, caches, pins and the GitLab pipeline stay as they are. Each publication of
`dev`, each proposal and each release of `main` starts the GitHub workflow by itself, so a manual
dispatch is no longer part of publication. `tasks.md` is the sole progress ledger.
