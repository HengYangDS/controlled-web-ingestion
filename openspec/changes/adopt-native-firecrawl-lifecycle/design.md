## Context

The Firecrawl route is an on-demand, disposable, loopback-only service. Its old lifecycle mixed
three owners: Homebrew for Redis and RabbitMQ, Compose for the Firecrawl containers, and Bash for
health, timeouts and teardown. The new lifecycle gives Compose the topology and health, and gives
the product the request lifecycle.

## Decisions

1. Run Redis and RabbitMQ as Compose services instead of host processes. Compose then owns their
   isolation, health and removal, and the project no longer needs host formulae, generated
   configuration, EPMD cleanup or extra loopback ports. Firecrawl's own Compose topology runs them
   the same way.
2. Reference every image by its reviewed digest and keep `pull_policy: never`. A digest reference
   is content-addressed, so `docker compose pull` acquires exactly the reviewed objects, and a run
   never pulls. The verifier still compares each local image ID and platform before startup.
3. Gate readiness on healthchecks and `docker compose up --wait --wait-timeout`. This replaces port
   polling and the separate timeout helper. The product still starts each Compose call in its own
   process group and terminates that group at its deadline or on interruption, so an interrupted
   `up` cannot race teardown. This is the minimal process glue that a caller-owned deadline needs.
4. Keep the stage in process. The runtime yields the loopback endpoint to the existing controller,
   so the private `--internal-firecrawl-stage` re-entry and its request file disappear.
5. Put workload validation in the product as `web-ingest validate-workloads`. It reads only the
   reviewed allowlist, calls the same product functions as users, and writes one body-redacted
   evidence record that the evidence schema validates.
6. Leave engine selection to the operator. Docker's own `DOCKER_CONTEXT` selects the engine; the
   product names no host or context.

## Risks

- RabbitMQ 4.3 replaces the formula that ran in July. The real run is the acceptance for that
  version with Firecrawl 2.10.19.
- Docker Hub is reachable here only through the engine's network path. The digests make transport
  irrelevant to integrity, but an unreachable registry blocks acquisition, not runs.

## Rollback

Revert this change. The Bash controllers, the importer and the host-process topology return
unchanged, and the July runbook applies again.
