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
