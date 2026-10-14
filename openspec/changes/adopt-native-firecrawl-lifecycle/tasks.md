# Tasks

## 1. Topology

- [x] 1.1 Declare Redis and RabbitMQ as Compose services, reference every image by its reviewed
      digest and gate the API on healthy stores; done when `docker compose config` renders only
      `127.0.0.1:13002` as a published port.
- [x] 1.2 Record the two added images in the provenance file and verify local images by digest;
      done when the verifier accepts the pulled set and rejects identity drift.

## 2. Product lifecycle

- [x] 2.1 Add the Compose-owned runtime to `web-ingest` and stage browser and crawl requests in
      process; done when unit tests cover startup, teardown after failure and the zero-resource
      check.
- [x] 2.2 Add `web-ingest validate-workloads --evidence PATH`; done when unit tests cover receipt
      assertions and the evidence record validates against the evidence schema.
- [x] 2.3 Remove the Bash controllers, `compose_with_timeout.py`, `verify-firecrawl-provenance.py`,
      the GHCR importer, its image list and library, and their tests; done when no tracked file
      outside dated evidence names them.

## 3. Verification

- [x] 3.1 Run strict OpenSpec validation and the repository gates; done when both pass.
- [x] 3.2 Run `web-ingest validate-workloads` against the reviewed allowlist; done when its
      evidence record is committed and no project resource remains.
