---
subject: controlled-web-ingestion:admission
role: reference
state: active
relations:
  canonical_for: future controlled-ingestion admission packet
  governed_by: docs/decisions/dr-0004-controlled-web-ingestion-position.md
  runtime: docs/reference/runtime-validation.md
---

# Admission Packet

An admission packet is required before any new target, purpose, data class,
route, runtime topology, or delivery sink is used. The existing allowlist and
runtime receipt are not blanket authority.

## Required packet

| Field | Required decision evidence |
| --- | --- |
| Target and owner | Canonical target identity, accountable owner, public-access basis, and an explicit statement that the target is not inherited from another packet. |
| Purpose | Narrow business or research purpose, expected outcome, and the reason the existing approved workload cannot satisfy it. |
| Data class | Allowed metadata and derived artifacts, prohibited content classes, retention, deletion, and access boundary. Credentials, account state, and private-target access are outside this capability. |
| Budget | Route, page limit, concurrency, timeout, retry and cost limits, plus a stop condition. |
| Robots and MIME | Preflight robots decision, allowed MIME classes, redirect handling, and service-returned final-target revalidation. |
| Route and sink | `static`, `browser`, or `crawl` route; staging and promotion decision; sink remains `null` unless a separately reviewed delivery adapter is admitted. |
| Runtime topology | Exact image and provenance identity where applicable, ports, isolation, teardown, dependencies, and whether the change affects the disposable loopback runtime. |
| Proof plan | Required policy/schema tests, route-specific verification, redacted receipt, cleanup evidence, local matrix, and independent GitHub Actions plus GitLab CI evidence when code changes are proposed. |

## Decision rule

The packet must be reviewed before implementation or execution. Any missing
field is a rejection, not an invitation to infer the answer from an existing
Firecrawl run. A packet that changes a target, data class, topology, or sink is
a separate admission even when its code change appears small.

## Verification rule

The resulting proof must be proportional to the proposed change and must keep
evidence classes distinct. A local unit test cannot substitute for a required
runtime proof; a runtime receipt cannot substitute for either hosted CI plane;
and GitHub Actions or GitLab CI cannot authorize a target or a new
data-retention boundary. All durable
artifacts remain body-redacted.

## Explicit non-admissions

This packet does not authorize a standing service, direct Firecrawl API access,
MCP exposure, default Agent tooling, Hermes or Open WebUI integration, a direct
RAG writer, credentials, private targets, or automatic synchronization. Each
would require its own control-plane and data-governance decision.
