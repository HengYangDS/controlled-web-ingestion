# Controlled Web Ingestion

A policy-bound, evidence-driven ingress capability for explicitly authorized
public web sources. It proves admission, acquires through a replaceable
adapter, and emits only a body-redacted receipt. It is not a standing crawler,
content store, RAG writer or framework showcase.

```text
intent -> policy -> route -> acquisition -> receipt -> promotion -> bridge -> evidence
```

## Boundary

- Firecrawl is on-demand, disposable and loopback-only; it is one adapter, not
  the repository identity.
- Crawl4AI, Crawlee, Scrapy plus Trafilatura, and Jina Reader are comparison or
  adapter candidates in the benchmark evidence lane.
- Raw bodies, HTML, Markdown, raw responses, credentials, private targets and
  account state never enter tracked receipts, evidence or Git history.
- No default MCP/Agent tool, Hermes/Open WebUI integration, direct RAG sink,
  shared listener or persistent crawler is authorized.
- GitHub and GitLab are independent, complete repository and CI/CD planes;
  neither is a snapshot or substitute for the other.

## Start

```bash
uv run --locked web-ingest --help
uv run --locked python tools/ci/run_tests.py
uv run --locked python tools/ci/validate_schemas.py
```

Read [the start guide](docs/start/README.md), then the
[topology](docs/architecture/controlled-web-ingestion-topology.md),
[contracts](docs/reference/contracts.md),
[Research contract](docs/reference/research-contract.md), and
[evidence index](docs/evidence/README.md).
