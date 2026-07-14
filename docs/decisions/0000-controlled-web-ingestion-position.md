---
subject: controlled-web-ingestion:position
role: decision
state: accepted
relations:
  canonical_for: repository identity and non-goals
  implemented_by: docs/architecture/controlled-web-ingestion-topology.md
---

# Decision 0000: Controlled Web Ingestion is the repository identity

## Decision

This repository is **Controlled Web Ingestion**. Its canonical project name is
`controlled-web-ingestion`; its prose name is *Controlled Web Ingestion*.

## Context and alternatives

A flat benchmark repository lets its candidate frameworks appear to own the
system. That is backwards: Firecrawl, Crawl4AI, Crawlee, Scrapy plus
Trafilatura, and Jina Reader are replaceable adapters or measured baselines.

- **Accepted — controlled ingress capability.** Policy, proof, redacted receipt
  and explicit promotion form the durable system boundary.
- **Rejected — Firecrawl-centered service.** It would turn an optional,
  disposable loopback adapter into an implicit shared dependency.
- **Rejected — benchmark product.** Candidate comparisons remain valuable
  evidence, but not the user's operational entry point or repository identity.

## Consequences

`src/web_ingestion/` owns runtime contracts; `system/` holds reviewed truth;
`tools/benchmark/` owns comparison evidence. No default MCP, Agent tool,
Hermes/Open WebUI integration, standing daemon or direct RAG writer is
permitted. Revisit only if a new integration surface is proposed with new
policy, schema, runtime and hosted evidence.
