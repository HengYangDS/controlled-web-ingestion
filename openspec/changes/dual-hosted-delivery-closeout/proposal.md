# Dual-hosted delivery publication closeout

## Why

The local delivery projection has been archived into its canonical OpenSpec
specification, but the release is not complete: GitHub and GitLab still need
their own repository identity, protected-main path, hosted CI execution, and
publication receipt. The active claim therefore needs a live carrier that
tracks those remaining facts without treating local proof as a substitute.

## What Changes

- Rebind the active dual-hosted delivery claim to this follow-on carrier and
  preserve its digest-bound local proof as local evidence only.
- Require independently observed GitHub and GitLab candidate parity, hosted CI,
  protection, and protected-main publication before release completion.
- Record each unavailable platform, missing eligible runner, or failed hosted
  job as a platform-specific block; do not recover by using a personal
  standing runner, direct push, mirror semantics, or cross-platform automation.

## Affected capabilities

- `delivery-governance`: subject=controlled-web-ingestion:delivery-governance;
  reuse=extend; change=modify; facet:lifecycle=publication;
  facet:surface=github-actions-and-gitlab-ci; facet:authority=repository-governance

## Impact

The change affects OpenSpec lifecycle carriers, claim/evidence bindings, hosted
delivery documentation, and CI projections only. It does not expand targets,
data classes, Firecrawl runtime topology, persistence, MCP, Hermes/Open WebUI,
or RAG surfaces.

## Out of Scope

- No Firecrawl runtime execution, image change, daemon, target expansion, or
  direct RAG delivery.
- No direct push to either protected `main`, automatic mirror, or automatic
  cross-platform publication.
- No registration, modification, reuse, or removal of a personal GitLab runner.
- No GitHub or GitLab hosted success is claimed until that platform's own
  repository, protection, candidate, and execution evidence has been observed.
