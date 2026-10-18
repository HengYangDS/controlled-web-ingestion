# Change: Adopt The Toolchain Owner And The CI Model

## Why

The ETHOS repository paradigm requires a locked toolchain owner that exposes the common
`bootstrap`, `check` and `fix` verbs, one CUE model for pipelines that run on more than one
Forge, and CI steps that each run one native command. This repository has no toolchain owner,
writes its GitHub workflow and GitLab pipeline by hand, and runs two multi-command GitHub steps,
so the paradigm report names four gaps.

## What Changes

- Add `.config/mise/config.toml` with locked resolution, the tools that the repository's checks
  already use at their current versions, and the `bootstrap`, `check` and `fix` tasks, and track
  the lock that `mise lock` writes.
- Model both pipelines once in `.config/ci/pipeline.cue`. `tools/ci/project.py` renders
  `.github/workflows/verify.yml` and `.gitlab-ci.yml` from it with the locked CUE, and its
  `--check` mode, a new proof gate, fails when a tracked projection differs.
- Run each GitHub step as one native command.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

Both CI files become generated projections and lose their YAML comments, which move into the
model. GitHub keeps the same jobs and commands, now one step each. The GitLab pipeline keeps its
jobs, images and runner selection. Hosted acceptance of both pipelines follows the landing.
`tasks.md` is the sole progress ledger.
