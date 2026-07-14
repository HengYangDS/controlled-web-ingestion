---
subject: controlled-web-ingestion:runtime-validation-2026-07-14
role: evidence
state: active
relations:
  evidence: evidence/verification/2026-07-14-controlled-web-ingestion-runtime-validation.json
---

# Runtime Validation — 2026-07-14

The final authorized run passed provenance and zero-resource preflight, static
ingestion, duplicate refusal, explicit promotion, sinkless bridge preparation,
browser ingestion, and the ten-page single-concurrency crawl. A deliberate
private-loopback browser request exited nonzero; the runner then left zero
label-bound containers, volumes, networks and benchmark listeners.

The runtime gate is therefore **passed for the exact allowlisted workload**.
It does not authorize arbitrary targets, a standing Firecrawl service, MCP,
default-Agent, Hermes, Open WebUI, or direct RAG integration. Hosted GitLab CI is a separate evidence class; it is neither run nor inferred by
this runtime receipt.
