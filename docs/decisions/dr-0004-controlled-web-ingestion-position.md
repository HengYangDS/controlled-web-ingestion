---
subject: controlled-web-ingestion:position
role: decision
state: canonical
decision_id: DR-0004
decision_status: accepted
relations:
  canonical_for: repository identity and non-goals
  implemented_by: docs/architecture/controlled-web-ingestion-topology.md
---

# DR-0004: Controlled Web Ingestion is the repository identity

This record was numbered 0000 until 2026-10-14. Decision identities are
positive numbers, so it took the next unused one; no other record changed.

## Context

A flat benchmark repository lets its candidate frameworks appear to own the
system. That is backwards: Firecrawl, Crawl4AI, Crawlee, Scrapy plus
Trafilatura, and Jina Reader are replaceable adapters or measured baselines.

## Decision

This repository is **Controlled Web Ingestion**. Its canonical project name is
`controlled-web-ingestion`; its prose name is _Controlled Web Ingestion_.

It is a controlled ingress capability: policy, proof, redacted receipt and
explicit promotion form the durable system boundary.

## Alternatives Rejected

- **Firecrawl-centered service:** rejected because it would turn an optional,
  disposable loopback adapter into an implicit shared dependency.
- **Benchmark product:** rejected because candidate comparisons remain valuable
  evidence, but not the user's operational entry point or repository identity.

## Consequences and Boundary

`src/web_ingestion/` owns runtime contracts; `system/` holds reviewed truth;
`tools/benchmark/` owns comparison evidence. No default MCP, Agent tool,
Hermes/Open WebUI integration, standing daemon or direct RAG writer is
permitted.

## Evidence and Revisit

Revisit only if a new integration surface is proposed with new policy, schema,
runtime and hosted evidence.
