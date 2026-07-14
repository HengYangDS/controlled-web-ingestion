---
subject: controlled-web-ingestion:ethos-adopter-boundary
role: decision
state: accepted
relations:
  canonical_for: ETHOS adoption authority boundary
  references: docs/reference/research-contract.md
---

# Decision 0001: Adopt ETHOS as governance, not runtime ownership

## Decision

Controlled Web Ingestion is an ETHOS adopter. ETHOS governs the delivery loop:

```text
orient -> status -> plan -> prove -> land -> publish
```

The repository retains domain authority over policy/redaction, schemas,
adapter routing, Firecrawl provenance, runtime teardown, Python matrix, and
evidence classification.

## Rationale

ETHOS supplies semantic discipline and a portable proof cycle. Copying its
product topology, packages, claims store, or runtime state would make this
small capability less legible and less portable. The adapter boundary therefore
uses only reviewed `.ethos/` and `openspec/` governance files; the Python
package has no ETHOS runtime import.

## Revisit trigger

Revisit if ETHOS can no longer execute a fail-closed Python plus GitLab overlay,
or if adoption asks to overwrite repository-owned contracts. A conflict in
`ethos adopt --dry-run` is a stop condition, not a reason to force apply.
