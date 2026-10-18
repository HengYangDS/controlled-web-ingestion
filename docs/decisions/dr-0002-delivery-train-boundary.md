---
subject: controlled-web-ingestion:delivery-train-boundary
role: decision
state: canonical
decision_id: DR-0002
decision_status: accepted
relations:
  canonical_for: ETHOS branch-role and protected publication boundary
  governed_by: docs/decisions/dr-0001-ethos-adopter-boundary.md
---

# DR-0002: Separate the published root from the ETHOS authoring train

## Context

The prior profile mapped both release and accepted roles to `main`, while also
declaring the retired topology work branch as candidate. The roles then became
indistinguishable to ETHOS: a clean protected root could not mint a lane, and
recreating the retired branch as a candidate would misrepresent its history.

## Decision

`main` remains the protected published release root. ETHOS uses three distinct
local delivery roles, in this order: `dev`, then `candidate/dev`, then one
`work/*` branch for each bounded change.

The ETHOS repository paradigm fixes these names. On 2026-10-15 accepted closeout
renamed the former `accepted/controlled-web-ingestion` and
`candidate/controlled-web-ingestion` refs to them.

The candidate branch is the sole review source. It may advance only through an
owned, proven Work Lane. On publication, the same reviewed candidate head is
presented through both independent forges; each platform's `main` advances only
through its own protected review and hosted CI path.

## Alternatives Rejected

- **Mapping the release and accepted roles to `main`:** rejected because the
  roles became indistinguishable and a clean protected root could not mint a
  lane.
- **Recreating the retired topology branch as the candidate:** rejected because
  it would misrepresent that branch's history.

## Consequences and Boundary

Separating delivery roles restores a fail-closed lifecycle without adding a
runtime environment or a standing service.

- The bootstrap commit establishes only the branch-role contract; it does not
  broaden any acquisition policy or Firecrawl authorization.
- Bootstrap creates the accepted and candidate refs from the merged release
  head after this decision is published. Subsequent work starts in an ETHOS
  Work Lane and carries its local lease.
- GitHub Actions and GitLab CI both remain required before their respective
  protected `main` publications. A platform or runner outage is recorded as an
  external blocker, never bypassed by direct pushes or a personal ad-hoc CI
  service.

## Evidence and Revisit

Revisit only if either forge's protected-branch model or ETHOS lane semantics
change. A desire for a shorter branch graph is not sufficient reason to merge
release and accepted roles again.
