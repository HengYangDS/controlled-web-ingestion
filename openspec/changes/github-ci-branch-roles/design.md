# Design

## Context

`.config/ci/pipeline.cue` owns both pipelines, and `tools/ci/project.py` renders
`.github/workflows/verify.yml` and `.gitlab-ci.yml` from it. The ETHOS repository paradigm fixes
the branch roles: release `main`, accepted `dev`, candidate `candidate/dev`, Work Lanes under
`work/` and proposals under `proposal/`. ETHOS publishes `dev` and `proposal/<slug>` refs to both
peers. Without `[release] mirror = "accepted_ff"` in `.ethos/release.toml`, `main` moves only when
a release selects it. The GitLab workflow rules run every push and web pipeline, so only the GitHub
projection depends on branch names.

## Goals / Non-Goals

**Goals:**

- Start the GitHub workflow for every ref that ETHOS publishes: the accepted branch, each proposal
  and the release branch.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, caches, pins or the GitLab rules.
- Mirroring `main` to `dev`. Whether the release branch follows the accepted branch is a separate
  release decision.

## Decisions

### Push triggers follow the published roles

`push: branches: ["dev", "main", "proposal/**"]` covers the accepted branch, the release branch and
every proposal. `candidate/**` goes, because the candidate role is local and is never published.

### Pull requests to the accepted branch run the same checks

`pull_request: branches: ["dev", "main"]` gives a proposal's pull request to `dev` its checks.
GitHub counts `pull_request` and `push` check suites in a commit's status rollup, unlike
`workflow_dispatch` suites. Pull requests to `main` keep their existing trigger.

### The contract test names the roles exactly

The CI contract test already reads the rendered projection as text. It now requires the two
trigger blocks verbatim and the absence of `candidate/`, so a regression in the model fails the
test, and `tools/ci/project.py --check` keeps the projection equal to the model.

## Risks / Trade-offs

- A proposal push and the later `dev` push at the same head each start a run. GitLab already runs
  both, and each published ref keeps its own evidence instead of borrowing a run of another ref.
- GitHub can still fail to start a push run, as it has for another repository published the same
  way. A manual dispatch stays available as the fallback, and publication checks that a run exists
  for the published head.
