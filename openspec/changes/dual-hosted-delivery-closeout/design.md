# Design

## Carrier lifecycle

`2026-07-15-dual-hosted-delivery` is the archived local projection carrier.
This closure carrier repairs its archive ledger and records final local proof.
It is then archived before candidate integration. Outstanding hosted
publication facts live in the canonical delivery-governance requirements,
decision, and publication reference; an integration branch must not retain an
active planning carrier merely because an external platform is unavailable.

## Evidence model

The dated local receipt remains digest-bound and names the exact source head
that was locally verified. Claim freshness uses only its declared semantic
scope, excluding the claim and receipt themselves. While this closure carrier
is active, the claim points to it; after archival, the claim points to its
archived path. GitHub and GitLab receipts are separate future evidence: neither
may infer, replay, or stand in for the other.

## Failure and rollback

An unavailable forge, missing eligible shared runner, failed hosted job,
candidate mismatch, or absent protection blocks only that platform's
publication. The response is to retain the block and evidence, not to broaden
runtime scope or create a local permanent executor. Reverting this change
restores the archive ledger and its prior claim binding; it does not erase
dated receipts or weaken canonical hosted-publication obligations.
