---
subject: controlled-web-ingestion:evidence
role: evidence
state: active
relations:
  canonical_for: proof classification and evidence admission
---

# Evidence Index

Evidence is body-redacted, versioned proof—not a content cache.

| Lane | Location | Purpose |
| --- | --- | --- |
| Candidate comparison | `evidence/benchmarks/` | Framework/adaptor measurement and historical admission evidence |
| Verification | `evidence/verification/` | Local matrix, security, schema, runtime, ETHOS, GitLab and closeout receipts |
| Curated chronicle | `docs/evidence/chronicle/<date>/` | Human-readable interpretation of dated proof; it does not replace machine receipts |
| Generated runtime output | ignored `results/` or temporary roots | Disposable diagnostics; never a tracked result by default |

Every committed JSON evidence record validates the tracked `evidence` schema
and rejects body, HTML, Markdown, raw response, credentials and private-target
fields recursively. Historical records are not rewritten; interpretation and
current status belong in dated closeout documents.

## Dated Interpretations

- [Runtime validation — 2026-07-14](chronicle/2026-07-14/runtime-validation.md)
- [Local proof — 2026-07-14](chronicle/2026-07-14/local-proof.md)
