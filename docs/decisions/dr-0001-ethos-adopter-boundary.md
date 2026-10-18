---
subject: controlled-web-ingestion:ethos-adopter-boundary
role: decision
state: canonical
decision_id: DR-0001
decision_status: accepted
relations:
  canonical_for: ETHOS adoption authority boundary
  references: docs/reference/research-contract.md
---

# DR-0001: Adopt ETHOS as governance, not runtime ownership

## Context

ETHOS supplies semantic discipline and a portable proof cycle. It also carries
its own product topology, packages, claims store and runtime state, while
Controlled Web Ingestion is a small capability with its own domain authority.

## Decision

Controlled Web Ingestion is an ETHOS adopter. ETHOS governs the delivery loop
of orient, status, plan, prove, land and publish.

The repository retains domain authority over policy/redaction, schemas,
adapter routing, Firecrawl provenance, runtime teardown, Python matrix, and
evidence classification.

## Alternatives Rejected

- **Copying the ETHOS product topology, packages, claims store or runtime
  state:** rejected because it would make this small capability less legible
  and less portable.

## Consequences and Boundary

The adapter boundary uses only reviewed `.ethos/` and `openspec/` governance
files; the Python package has no ETHOS runtime import.

## Evidence and Revisit

Revisit if ETHOS can no longer execute fail-closed Python plus GitHub and
GitLab delivery projections, or if adoption asks to overwrite repository-owned
contracts. A conflict in an adoption dry run is a stop condition, not a reason
to force apply.
