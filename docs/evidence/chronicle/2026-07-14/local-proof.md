---
subject: controlled-web-ingestion:local-proof-2026-07-14
role: evidence
state: active
relations:
  evidence: evidence/verification/2026-07-14-controlled-web-ingestion-local-proof.json
  runtime: evidence/verification/2026-07-14-controlled-web-ingestion-runtime-validation.json
---

# Local Proof — 2026-07-14

At the verified repository head, Python 3.12, 3.13 and 3.14 each passed all
66 tests through the owner CI command. Schema, documentation, source-topology,
Gitleaks and Firecrawl provenance gates also passed.

The explicit Firecrawl runtime receipt remains a separate, successful proof for
the unchanged runtime implementation: provenance, static ingestion, duplicate
rejection, explicit promotion, a `sink: null` bridge, browser, a ten-page
single-concurrency crawl, private-loopback rejection and zero-resource teardown
all passed. It authorizes no target or integration beyond that allowlisted,
disposable loopback workload.

GitLab pipeline `2673` separately passed its four required jobs on runner
`34`: Python 3.12, 3.13, 3.14 and security. It executed commit
`68760e252781a6b1149a27f748df26a5df4804f8`; because this receipt is created
at a later head, the receipt records that distinction rather than projecting the
older hosted result forward. A fresh pipeline for the final evidence head is
required before protected-branch publication.
