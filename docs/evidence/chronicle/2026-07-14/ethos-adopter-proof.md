---
subject: controlled-web-ingestion:ethos-adopter-proof-2026-07-14
role: evidence
state: active
relations:
  proof: .ethos/state/proof/60b1d4615251ccf9450c68836d6ffd910a6b0cd4.json
  decision: docs/decisions/0001-ethos-adopter-boundary.md
---

# ETHOS Adopter Proof — 2026-07-14

ETHOS was invoked with an explicit repository root and expected head
`60b1d4615251ccf9450c68836d6ffd910a6b0cd4`. The repository-scoped adopter proof executed successfully with no
required gaps. Its local machine-state receipt is intentionally ignored rather
than committed:

```text
.ethos/state/proof/60b1d4615251ccf9450c68836d6ffd910a6b0cd4.json
sha256:6cb7fce62fb9705fcc158cd163d55b51c14e0bfa69543e73e7165d90d97561e5
```

The proof ran the adopted repository's native behavior and static-analysis
gates, plus the ETHOS governance, schema, document, generated-artifact,
evidence-freshness and repository-audit gates. It is governance evidence only:
ETHOS does not become a runtime dependency, a Firecrawl controller or a source
of authority over this repository's policy, schema, runtime or receipt truth.
