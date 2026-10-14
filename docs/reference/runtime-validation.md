---
subject: controlled-web-ingestion:runtime-validation
role: reference
state: active
relations:
  canonical_for: Firecrawl admission and teardown proof
---

# Runtime Validation

Full Firecrawl proof is deliberately separate from generic CI. It requires the reviewed local
images, a Docker engine, explicit runtime authorization and the fixed public workload declaration.

Acquire the reviewed images once. Every image in the Compose projection is a digest reference, so
the pull fetches exactly the reviewed objects:

```bash
docker compose --file system/projections/firecrawl-isolated-compose.yaml pull
```

Then run the authorized workload set and name the evidence record:

```bash
uv run --locked web-ingest validate-workloads --evidence ABSOLUTE_PATH
```

Docker's own `DOCKER_CONTEXT` selects the engine; the repository names none.

Each browser or crawl request verifies every local image ID and platform against
`system/supply-chain/firecrawl-provenance.json`. It then starts the whole topology with
`docker compose up --wait`. Redis, RabbitMQ and Postgres are healthy before the API starts, and
only `127.0.0.1:13002` is published. After the request, the project is removed with its volumes,
and the run fails unless no project container, volume, network or listener remains. Every Compose
call has a caller-owned deadline that ends its whole process group, so an interrupted startup
cannot outlive teardown.

The validation also checks the duplicate, promotion and sinkless bridge steps. It asks the running
service to scrape a loopback address and requires a refusal. It then fails a private request inside
a running topology and requires teardown to complete anyway. The evidence record is written only
after every check passes; it holds digests and decisions, never bodies.

The allowlisted ten-page serial crawl has a 120-second total budget; it remains bounded by the
runtime contract and does not increase page or concurrency limits. A missing image, unavailable
engine, failed workload, or failed cleanup leaves the gate open; none authorizes a fallback daemon
or weaker policy.
