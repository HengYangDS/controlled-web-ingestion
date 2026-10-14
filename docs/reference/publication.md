---
subject: controlled-web-ingestion:publication-boundary
role: reference
state: active
relations:
  canonical_for: portable publication and evidence boundary
---

# Publication Boundary

This repository is a portable, body-redacted publication of Controlled Web
Ingestion. It includes source, reviewed declarations, schemas, tests,
documentation and curated evidence. It excludes raw responses, credentials,
mutable logs, virtual environments, caches, container state and private runtime
configuration.

GitHub and GitLab are independent complete repository and CI/CD planes. Each
must contain the same reviewed candidate head before publication and must record
its own protected-main review and hosted verification result. Neither platform
is a snapshot, mirror, or substitute for the other; see
`docs/decisions/dr-0003-dual-hosted-delivery.md`.
