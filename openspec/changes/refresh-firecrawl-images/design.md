# Design

## Context

`system/supply-chain/firecrawl-provenance.json` binds each of the five images in the isolated
Firecrawl topology to a reviewed manifest digest, a local image identity and a verification method.
`system/projections/firecrawl-isolated-compose.yaml` references the same digests with
`pull_policy: never`, and `web-ingest` refuses to start unless every local image matches its record.
Firecrawl builds an API image from every main commit and tags it `<major>.<minor>.<build>`, with a
`-production` twin and a `sha-<commit>-linux-<arch>` tag; the images carry no source-revision label.
The Playwright service and NuQ Postgres images publish only a moving `latest` tag and `sha-` tags.
On 25 October 2026 the registries, the GitHub releases API and the release tree were read for this
Change.

## Goals / Non-Goals

**Goals:**

- Run the API image that belongs to the newest stable Firecrawl release, and the current stable
  RabbitMQ and Redis images.

**Non-Goals:**

- Changing services, environment, limits, listeners, health checks or the workload set.
- Moving the Playwright service and NuQ Postgres images.

## Decisions

### The API follows the release, not the newest build

v2.11.0, published on 19 June 2026, is the newest stable release. The build of its commit,
`sha-ef12eb36b2f3-linux-arm64`, has the linux/arm64 manifest that 2.10.30 carries, so 2.10.30 is
the release image. The newest build, 2.11.209 from 18 August 2026, comes from main after the
release, and no release contains it. The release harness still reads `NUQ_WORKER_COUNT`, so the
Compose comment about the single NuQ worker carries over with the new version.

### The Playwright service and NuQ Postgres keep their reviewed digests

Both repositories keep `sha-` tags only from 19 October 2026 onward, and every one of those commits
comes after v2.11.0, so no tagged build belongs to the release. GHCR still serves both reviewed
digests. Moving them to `latest` would pair unreleased companion builds with the release API, so
the runtime acceptance pairs the release API with the reviewed companions instead.

### RabbitMQ and Redis take the current Docker Official Images

RabbitMQ 4.4.0 is the newest stable 4.x Alpine image. Redis 8.10.2 is still the newest 8.x Alpine
release, and its tag now resolves to a republished index. Both stay pinned by index digest, and the
engine resolves linux/arm64/v8 as before.

### The runtime acceptance proves the set works together

Unit tests cannot show that the moved images work with the rest of the topology.
`web-ingest validate-workloads` runs the reviewed static, browser and crawl workloads against the
pulled set, checks the loopback refusal and the cleanup, and writes its evidence record only after
every check passes.

## Risks / Trade-offs

- [The release API may not work with the reviewed companion builds] → The runtime acceptance drives
  the browser workload through the Playwright service and the crawl through NuQ Postgres; a failure
  keeps the reviewed set.
- [A registry may stop serving a pinned digest] → GHCR serves all three reviewed Firecrawl digests
  today. A missing object blocks acquisition, never integrity, because every reference is a digest.

## Rollback

Revert this Change. The reviewed digests return, and `docker compose pull` acquires them again.
