# Tasks

## 1. Python lock

- [x] 1.1 Refresh `uv.lock` with `uv lock --upgrade`; done when OSV reports no advisory in the refreshed lock that a stable release fixes and every `mise run check` command passes on the refreshed environment. `uv lock --upgrade` moves anyio 4.16.0, cachetools 7.2.8, filelock 4.2.6, openai 3.42.1, platformdirs 4.14.3 and python-dateutil 4.0.0, and drops six. OSV reports only scrapy's PYSEC-2017-83, which has no fixed release, and all nine commands pass, with 89 tests.

## 2. TLS trust

- [x] 2.1 Require in the transport contract test that `default_transport` refuses a certificate that the host's trust accepts and the locked roots do not hold, and make it verify against `certifi`; done when the test fails before the change and passes after it, and `docs/reference/contracts.md` states the contract. On the old transport the test failed with `URLError not raised` after its control request returned 200, and it passes on the new one. `validate-workloads` runs as documented, with no `SSL_CERT_FILE`.

## 3. Firecrawl RabbitMQ

- [x] 3.1 Record the republished `rabbitmq:4.4.0-alpine` index digest in `system/supply-chain/firecrawl-provenance.json` and pin it in `system/projections/firecrawl-isolated-compose.yaml`; done when the runtime unit test that compares both files passes, and `docker compose pull --policy always` returns the recorded identity, which `web-ingest` accepts. The provenance test passes. The pull returned local image ID `sha256:cc9d78f17950` on linux/arm64, the ID the old index gave, and the validation run accepted all five images.
- [x] 3.2 Run `web-ingest validate-workloads` against the moved set; done when its evidence record is committed under `evidence/verification/` and no project resource remains. The run wrote `2026-11-02-controlled-web-ingestion-runtime-validation.json` and left no container, volume or network.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass.
