---
subject: controlled-web-ingestion:runtime-validation-2026-07-14
role: evidence
state: active
relations:
  evidence: evidence/verification/2026-07-14-controlled-web-ingestion-runtime-validation.json
---

# Runtime Validation — 2026-07-14

Image provenance and the zero-resource preflight passed. The authorized browser
case did not start: OrbStack's `docker compose up --detach` did not return
within the runner's 120-second bounded startup window, and no loopback API
listener became available. The runner's timeout recovery released all
label-bound containers, volumes, networks and benchmark listeners.

The runtime gate is therefore **open, not passed**. The evidence records a
bounded orchestration failure and cleanup, not a Firecrawl capability success.
