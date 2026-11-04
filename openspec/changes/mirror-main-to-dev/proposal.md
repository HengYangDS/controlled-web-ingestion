# Proposal

## Why

`.ethos/release.toml` declares no release mirror, so ETHOS treats `main` as an independent release
branch that moves only when a release is cut. The repository has never cut one: its version is
0.0.0 and it has no tag. So `main`, the default branch of the public GitHub repository and of the
GitLab project, has stayed at `afc677c` from 15 October 2026 while `dev` moved 52 commits ahead. On
4 November 2026 the owner decided that `main` follows `dev`, as it does in the other governed
repositories, and that each platform keeps the review path that DR-0002 and DR-0003 require.

## What Changes

- Declare `mirror = "accepted_ff"` under `[release]` in `.ethos/release.toml`, so every accepted
  closeout fast-forwards `main` together with `dev`.
- Record in DR-0002 and DR-0003 that `main` mirrors `dev`, and that each platform's `main` still
  advances only through its own reviewed change path: a GitHub pull request and a GitLab merge
  request from `dev` to `main`, whose hosted checks pass on the exact head before the fast-forward
  is published.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, and the delivery-governance requirement
for hosted CI and protected-main evidence on each platform stays as it is, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`.ethos/release.toml`, `docs/decisions/dr-0002-delivery-train-boundary.md` and
`docs/decisions/dr-0003-dual-hosted-delivery.md`. No version, tag, workflow, pipeline, ruleset or
branch protection changes. `tasks.md` is the sole progress ledger.
