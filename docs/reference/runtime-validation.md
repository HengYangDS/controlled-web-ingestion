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
down containers, volumes, networks, listeners and temporary Python state. A
missing image, unavailable dependency, or failure to clean up leaves the gate
open; it never authorizes a fallback daemon or weaker policy.
