# Dual hosted repository and CI/CD delivery

## Why

GitHub must no longer be treated as a source snapshot. Controlled Web Ingestion
requires GitHub and GitLab to be independent, complete repositories with their
own CI/CD and protected-publication evidence. The existing GitLab-only delivery
record cannot establish GitHub repository identity, Actions execution, branch
protection, or cross-forge candidate parity.

## What Changes

- **delivery-governance:** Add GitHub Actions as an independent, pinned, thin
  projection of repository-owned verification commands and record GitHub plus
  GitLab as equal hosted delivery planes.
- **delivery-governance:** Require independent hosted CI, protected-main
  publication evidence, and candidate-head parity for the two platforms.
- **delivery-governance:** Preserve the controlled-ingestion runtime boundary:
  this change does not add a target, data class, service, MCP, Hermes/Open WebUI,
  RAG sink, personal CI runner, or automatic cross-platform publication.

## Affected capabilities

- `delivery-governance`: subject=controlled-web-ingestion:delivery-governance;
  reuse=extend; change=modify; facet:lifecycle=publication;
  facet:surface=github-actions-and-gitlab-ci; facet:authority=repository-governance

## Out of Scope

- No Firecrawl runtime execution, image change, daemon, target expansion, or
  direct RAG delivery.
- No direct push to either protected `main` and no automatic mirroring.
- No registration, modification, reuse, or removal of a personal GitLab runner.
