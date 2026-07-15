---
subject: controlled-web-ingestion:delivery-train-boundary
role: decision
state: canonical
relations:
  canonical_for: ETHOS branch-role and protected publication boundary
  governed_by: docs/decisions/0001-ethos-adopter-boundary.md
---

# Decision 0002: Separate the published root from the ETHOS authoring train

## Decision

`main` remains the protected published release root. ETHOS uses distinct local
delivery roles:

```text
accepted/controlled-web-ingestion
  -> candidate/controlled-web-ingestion
  -> work/<bounded-change>
```

The candidate branch is the sole review source. It may advance only through an
owned, proven Work Lane. On publication, the same reviewed candidate head is
presented through both independent forges; each platform's `main` advances only
through its own protected review and hosted CI path.

## Rationale

The prior profile mapped both release and accepted roles to `main`, while also
declaring the retired topology work branch as candidate. The roles then became
indistinguishable to ETHOS: a clean protected root could not mint a lane, and
recreating the retired branch as a candidate would misrepresent its history.

Separating delivery roles restores a fail-closed lifecycle without adding a
runtime environment or a standing service.

## Consequences

- The bootstrap commit establishes only the branch-role contract; it does not
  broaden any acquisition policy or Firecrawl authorization.
- Bootstrap creates the accepted and candidate refs from the merged release
  head after this decision is published. Subsequent work starts through
  `ethos lane start` and carries its local lease.
- GitHub Actions and GitLab CI both remain required before their respective
  protected `main` publications. A platform or runner outage is recorded as an
  external blocker, never bypassed by direct pushes or a personal ad-hoc CI
  service.

## Revisit trigger

Revisit only if either forge's protected-branch model or ETHOS lane semantics
change. A desire for a shorter branch graph is not sufficient reason to merge
release and accepted roles again.
