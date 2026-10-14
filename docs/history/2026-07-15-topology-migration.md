---
subject: controlled-web-ingestion:topology-migration-2026-07-15
role: history
state: active
relations:
  canonical_for: migration map from M1-M5 experiment records to controlled-ingestion governance
  current_topology: docs/architecture/controlled-web-ingestion-topology.md
---

# Topology Migration Map — 2026-07-15

The M1-M5 records describe the admission experiment that established the
current controlled-ingestion boundary. They remain historical evidence and are
not rewritten. This map only supplies the current reading path.

| Historical lane | Retained historical record | Current canonical reading path |
| --- | --- | --- |
| M1 framework admission and Firecrawl recovery | `evidence/benchmarks/2026-07-14-web-ingestion-firecrawl-m1-closeout.md`; `evidence/benchmarks/2026-07-14-web-ingestion-firecrawl-m1-runtime.json` | `docs/architecture/controlled-web-ingestion-topology.md`; `docs/decisions/dr-0004-controlled-web-ingestion-position.md`; `docs/reference/runtime-validation.md` |
| M2 design | `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-design.md` | `docs/architecture/controlled-web-ingestion-topology.md`; `docs/reference/contracts.md` |
| M3-M5 implementation and operations | `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-implementation.md`; `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-runbook.md` | `docs/reference/cli.md`; `docs/reference/runtime-validation.md`; `system/` declarations and schemas |
| M2-M5 verification and retrospective | `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-closeout-retrospective.md`; dated benchmark receipts | `evidence/verification/2026-07-14-controlled-web-ingestion-local-proof.json`; `evidence/verification/2026-07-14-controlled-web-ingestion-runtime-validation.json`; `docs/evidence/README.md` |
| ETHOS adoption and delivery | dated chronicle records | `docs/decisions/dr-0001-ethos-adopter-boundary.md`; `docs/decisions/dr-0002-delivery-train-boundary.md`; `docs/start/adopter-governance.md` |

The migration does not turn old benchmark result files into current runtime
authorization. Current authority is distributed deliberately: the policy and
schemas define admissible work; the topology and decisions define boundaries;
dated receipts prove specific observations; this closeout records their limits.

Any future target, data class, runtime topology, or sink must follow
`docs/reference/admission.md`. It cannot inherit authorization merely because
an older M1-M5 record mentioned a related framework or route.
