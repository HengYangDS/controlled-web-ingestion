# Reconcile archived dual-hosted delivery records

## Why

The completed local delivery closure has been archived, but the final archive
move changes its canonical OpenSpec location and claim binding. Those tracked
reconciliation edits need one bounded active carrier so candidate integration
remains fully auditable.

## What Changes

- Rebind the active delivery claim to the archived local closure carrier.
- Preserve the fused local carrier requirement in the canonical
  delivery-governance specification.
- Archive this reconciliation carrier after current local verification.

## Affected capabilities

- `delivery-governance`: subject=controlled-web-ingestion:delivery-governance;
  reuse=extend; change=modify; facet:lifecycle=publication;
  facet:surface=github-actions-and-gitlab-ci;
  facet:authority=repository-governance

## Impact

Only OpenSpec lifecycle metadata, canonical delivery governance, and the
evidence claim are affected. No hosted publication is attempted or claimed.

## Out of Scope

- No GitHub or GitLab repository creation, push, CI execution, protection
  change, pull request, merge request, or protected-main publication.
- No Firecrawl runtime, allowlist, persistence, MCP, Hermes/Open WebUI, or RAG
  surface change.
