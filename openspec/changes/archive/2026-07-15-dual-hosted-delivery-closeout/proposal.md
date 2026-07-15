# Dual-hosted delivery publication closeout

## Why

The local delivery projection needs a valid archival record and a final
evidence-bound proof. GitHub and GitLab still need their own repository
identity, protected-main path, hosted CI execution, and publication receipt,
but those external operating facts must remain canonical release obligations,
not an active OpenSpec carrier that blocks the reviewed candidate from landing.

## What Changes

- Repair archive metadata and complete only the already-observed local proof
  tasks for prior carriers.
- Preserve the digest-bound local proof as local evidence only, and bind the
  active claim to this closure carrier until it is archived.
- Retain independently observed GitHub and GitLab candidate parity, hosted CI,
  protection, and protected-main publication as canonical release obligations.

## Affected capabilities

- `delivery-governance`: subject=controlled-web-ingestion:delivery-governance;
  reuse=extend; change=modify; facet:lifecycle=publication;
  facet:surface=github-actions-and-gitlab-ci; facet:authority=repository-governance

## Impact

The change affects OpenSpec lifecycle carriers and claim/evidence bindings
only. It does not expand targets, data classes, Firecrawl runtime topology,
persistence, MCP, Hermes/Open WebUI, or RAG surfaces.

## Out of Scope

- No Firecrawl runtime execution, image change, daemon, target expansion, or
  direct RAG delivery.
- No direct push to either protected `main`, automatic mirror, or automatic
  cross-platform publication.
- No registration, modification, reuse, or removal of a personal GitLab runner.
- No GitHub or GitLab hosted success is claimed until that platform's own
  repository, protection, candidate, and execution evidence has been observed.
- No hosted publication implementation occurs in this closure carrier.
