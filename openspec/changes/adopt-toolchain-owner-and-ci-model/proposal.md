# Change: Adopt The Toolchain Owner And The CI Model

## Why

The ETHOS repository paradigm requires a locked toolchain owner that exposes the common
`bootstrap`, `check` and `fix` verbs, one CUE model for pipelines that run on more than one
Forge, and CI steps that each run one native command. This repository has no toolchain owner,
writes its GitHub workflow and GitLab pipeline by hand, and runs two multi-command GitHub steps,
so the paradigm report names four gaps. The current ETHOS runtime also checks every decision
record against the shared decision grammar, which the four records here predate.

## What Changes

- Add `.config/mise/config.toml` with locked resolution, the tools that the repository's checks
  already use at their current versions, and the `bootstrap`, `check` and `fix` tasks, and track
  the lock that `mise lock` writes.
- Model both pipelines once in `.config/ci/pipeline.cue`. `tools/ci/project.py` renders
  `.github/workflows/verify.yml` and `.gitlab-ci.yml` from it with the locked CUE, and its
  `--check` mode, a new proof gate, fails when a tracked projection differs.
- Run each GitHub step as one native command.
- Restate the four decision records and their template in the shared decision grammar: a
  `DR-NNNN` identity and accepted status in front matter, a `DR-NNNN:` title and the five
  rationale sections in order, with the fenced diagrams and the command example written as
  prose.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

Both CI files become generated projections and lose their YAML comments, which move into the
model. GitHub keeps the same jobs and commands, now one step each. The GitLab pipeline keeps its
jobs, images and runner selection. The decision records keep their rulings and reasons, and
DR-0003 names the pipeline model as the source of both CI files. Hosted acceptance of both
pipelines follows the landing.
`tasks.md` is the sole progress ledger.
