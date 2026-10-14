## Why

Firecrawl runs are orchestrated by two Bash controllers under `tools/runtime/`. They start
Homebrew Redis and RabbitMQ as host processes with generated configuration, bound `compose up`
through a separate process-group helper, and poll ports with `curl` and `lsof`. They therefore run
only on a macOS host that carries those formulae, and they keep business and acceptance logic in
shell and inline Python. The repository owns cross-platform owner commands and admits no shell
orchestration.

Image supply depends on a custom GHCR range importer. It was written for a host whose GHCR streams
were truncated. On 2026-10-14, native `docker pull` of each reviewed platform manifest digest
returned images whose local IDs equal the reviewed IDs, so the recovery path has no remaining
necessity.

## What Changes

- The Compose projection declares the whole topology. Redis and RabbitMQ become services from the
  official `redis:8.10.2-alpine` and `rabbitmq:4.3.6-alpine` images. Every image is referenced by
  its reviewed digest, every store has a healthcheck, and the API starts only after its stores are
  healthy. The API's `127.0.0.1:13002` remains the only published port.
- `web-ingest` owns the runtime lifecycle. Each browser or crawl request verifies provenance,
  starts the topology with `docker compose up --wait`, stages the result in process, removes the
  project with `docker compose down --volumes --remove-orphans`, and verifies that no project
  container, volume, network or listener remains.
- `web-ingest validate-workloads --evidence PATH` replaces the M2-M5 Bash validation. It also
  checks that the running service rejects a loopback scrape target.
- The two Bash controllers, `compose_with_timeout.py`, `verify-firecrawl-provenance.py`, the GHCR
  importer with its image list and its library, and their tests are removed.
- This is a runtime topology change, so it carries a new admission review: provenance for the two
  added images and a real authorized run as evidence.

## Evidence Boundary

Local evidence: strict OpenSpec validation, the repository gates, the ETHOS proof in the Work Lane,
and one real authorized run of `web-ingest validate-workloads` on this host. Hosted CI does not run
the Firecrawl runtime.

## Non-goals

- No new target, data class, page budget, concurrency or delivery sink.
- No change to the Firecrawl API, playwright or nuq-postgres images.
- No standing service, daemon configuration change or registry mirror.
