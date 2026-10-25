# Proposal

## Why

`system/supply-chain/firecrawl-provenance.json` names Firecrawl release v2.11.0 as the source, but
its API image `ghcr.io/firecrawl/firecrawl:2.10.19` is a build from 16 June 2026, eleven builds
before that release's commit `ef12eb36b2f3`. The image built from the release commit is 2.10.30.
On 25 October 2026 v2.11.0 was still the newest stable Firecrawl release, RabbitMQ's newest stable
image was `4.4.0-alpine` against the reviewed `4.3.6-alpine`, and Redis had republished
`8.10.2-alpine` under a new index digest. Every image change needs the full runtime acceptance; the
user authorized it on 25 October 2026.

## What Changes

- Move the API image to `ghcr.io/firecrawl/firecrawl:2.10.30`, the build of the v2.11.0 release
  commit, pinned by its linux/arm64 manifest digest.
- Move RabbitMQ to `docker.io/library/rabbitmq:4.4.0-alpine` and Redis to the republished
  `docker.io/library/redis:8.10.2-alpine`, each pinned by its index digest.
- Keep the Playwright service and NuQ Postgres images at their reviewed digests.
- Record each moved image's digest, local image identity and verification in
  `system/supply-chain/firecrawl-provenance.json`, and pin the same digests in
  `system/projections/firecrawl-isolated-compose.yaml`.
- Commit the body-redacted record of `web-ingest validate-workloads` under `evidence/verification/`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The topology keeps its services, limits, listeners, workload set and source release. Operators
acquire the moved images once with `docker compose pull`, which fetches exactly the pinned objects.
The Playwright service and NuQ Postgres images stay as reviewed, and the design explains why.
`tasks.md` is the sole progress ledger.
