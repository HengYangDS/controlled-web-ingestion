---
subject: controlled-web-ingestion:contracts
role: reference
state: active
relations:
  canonical_for: policy, receipt, bridge and schema contract
---

# Contracts

The request contract requires URL, non-empty purpose, mode, page budget,
timeout and a caller-owned staging root. Every redirect hop, robots outcome,
MIME type, route budget and Firecrawl-reported final URL are admitted before a
receipt is persisted.

Tracked schemas under `system/schemas/` govern policy, authorized workloads,
routing, staged receipt, promoted receipt, bridge manifest and evidence. Stage
and bridge writers validate before writing. A duplicate can be staged for audit
but cannot be promoted; promotion and bridge preparation require confirmation.

No receipt, bridge manifest or evidence record may contain body, HTML,
Markdown, raw response, credentials, cookies, authorization values or a private
target.
