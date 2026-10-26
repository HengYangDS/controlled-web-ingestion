# Tasks

## 1. Image records

- [x] 1.1 Record the new API, RabbitMQ and Redis digests in `system/supply-chain/firecrawl-provenance.json` and pin the same digests in `system/projections/firecrawl-isolated-compose.yaml`; done when the runtime unit test that compares both files fails on the provenance change alone and passes with both. It failed on the RabbitMQ digest first and passes with both files.
- [x] 1.2 Acquire the moved images with `docker compose pull --policy always` and record their local image identities; done when `web-ingest` accepts the pulled set. The pull returned the recorded identities on linux/arm64, and the validation run accepted all five images.
- [x] 1.3 Name `docker compose pull --policy always` in the runtime validation reference, the topology document, the Compose comment and the provenance constraint; done when no live document names the plain pull. The plain pull skipped all five services under Docker Compose 5.6.1.

## 2. Runtime acceptance

- [x] 2.1 Run `web-ingest validate-workloads` against the new set; done when its evidence record is committed under `evidence/verification/` and no project resource remains. The first run stopped on a crawl that came back short of ten pages; a diagnostic crawl and the second run both returned ten. The second run wrote `2026-10-25-controlled-web-ingestion-runtime-validation.json` and left no container, volume, network or listener.
- [x] 2.2 Run strict OpenSpec validation and every `mise run check` command; done when both pass. Both pass, including the 88 tests.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- The lane moves onto the candidate after the stable supply and CI environment Changes land.
- Hosted acceptance follows publication.
