---
subject: controlled-web-ingestion:start
role: how-to
state: active
relations:
  canonical_for: first-run, contribution and evidence path
  governed_by: docs/architecture/controlled-web-ingestion-topology.md
---

# Controlled Web Ingestion

Controlled Web Ingestion is a policy-bound ingress capability for explicitly
authorized public web sources. It is neither a standing crawler nor a content
store. A request proceeds only through:

```text
intent -> policy -> route -> acquisition -> redacted receipt -> explicit promotion -> sinkless bridge -> evidence
```

## First proof

```bash
uv run --locked web-ingest --help
uv run --locked python tools/ci/run_tests.py
uv run --locked python tools/ci/validate_schemas.py
```

The only interactive data-plane command is `web-ingest`; it has `ingest`,
`promote`, and `prepare-rag` subcommands. Browser and crawl modes are routed
through the disposable, loopback-only Firecrawl runner. They require explicit
local runtime authorization and are not ordinary CI work.

## Read in this order

1. [Position decision](../decisions/0000-controlled-web-ingestion-position.md)
2. [Topology](../architecture/controlled-web-ingestion-topology.md)
3. [Contracts](../reference/contracts.md)
4. [CLI reference](../reference/cli.md)
5. [Runtime validation](../reference/runtime-validation.md)
6. [Evidence index](../evidence/README.md)
7. [ETHOS adopter governance](adopter-governance.md)
