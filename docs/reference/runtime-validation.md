---
subject: controlled-web-ingestion:runtime-validation
role: reference
state: active
relations:
  canonical_for: Firecrawl admission and teardown proof
---

# Runtime Validation

Full Firecrawl proof is deliberately separate from generic CI. It requires
reviewed local images, Homebrew-managed Redis and RabbitMQ, explicit runtime
authorization, and the fixed public workload declaration.

```bash
tools/runtime/validate-authorized-workloads.sh
```

The runner verifies provenance before Compose startup, binds only loopback
ports, starts no shared service, rejects a private-loopback target, and tears
down containers, volumes, networks, listeners and temporary Python state. Its
Compose invocation is process-group bounded and records the active child group
so an interrupted runner cannot leave a detached `compose up` behind. The
allowlisted ten-page serial crawl has a 120-second total budget; it remains
bounded by the runtime contract and does not increase page or concurrency
limits. A missing image, unavailable dependency, failed workload, or failed
cleanup leaves the gate open; none authorizes a fallback daemon or weaker
policy.
