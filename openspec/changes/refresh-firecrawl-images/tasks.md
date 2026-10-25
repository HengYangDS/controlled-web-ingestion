# Tasks

## 1. Image records

- [ ] 1.1 Record the new API, RabbitMQ and Redis digests in `system/supply-chain/firecrawl-provenance.json` and pin the same digests in `system/projections/firecrawl-isolated-compose.yaml`; done when the runtime unit test that compares both files fails on the provenance change alone and passes with both.
- [ ] 1.2 Acquire the moved images with `docker compose pull` and record their local image identities; done when `web-ingest` accepts the pulled set.

## 2. Runtime acceptance

- [ ] 2.1 Run `web-ingest validate-workloads` against the new set; done when its evidence record is committed under `evidence/verification/` and no project resource remains.
- [ ] 2.2 Run strict OpenSpec validation and every `mise run check` command; done when both pass.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- The lane moves onto the candidate after the stable supply and CI environment Changes land.
- Hosted acceptance follows publication.
