---
subject: controlled-web-ingestion:ethos-governance
role: how-to
state: active
relations:
  implements: docs/decisions/0001-ethos-adopter-boundary.md
---

# ETHOS Adopter Governance

Always bind ETHOS to this repository explicitly:

```bash
ethos orient --root <repository-root>
ethos status --root <repository-root>
ethos plan --root <repository-root>
ethos prove --root <repository-root>
```

Before apply, run both the Python and GitLab overlay adoption dry-runs against
the exact branch HEAD. Review every proposed path. Apply only a conflict-free,
head-bound plan with a rollback list. ETHOS proof is local governance evidence;
GitLab hosted CI remains a separate observation.

## Delivery train

`main` is the protected published release root. It is not used as an ETHOS
authoring root. The distinct train is:

```text
accepted/controlled-web-ingestion
  -> candidate/controlled-web-ingestion
  -> work/<bounded-change>
```

An owned `work/` lane is created from the clean candidate train, proven there,
then integrated into the candidate train. The candidate is the reviewed GitLab
MR source; publication advances only through the protected `main` merge. This
is a delivery distinction, not a long-lived development environment and does
not authorize a new runtime surface.

Bootstrap the accepted and candidate refs only after the delivery-topology
decision is merged to `main`; do not recreate a retired work branch as a
candidate or write directly to the release root.
