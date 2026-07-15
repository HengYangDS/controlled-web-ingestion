# Design

## Carrier lifecycle

`2026-07-15-dual-hosted-delivery` is the archived local projection carrier.
This follow-on carrier owns the remaining hosted publication facts. The active
claim points here while GitHub and GitLab evidence remains outstanding; it will
move to this carrier's archive only after both planes have independently
completed their protected publication paths.

## Evidence model

The dated local receipt remains digest-bound and names the exact source head
that was locally verified. Claim freshness uses only its declared semantic
scope, excluding the claim and receipt themselves. GitHub and GitLab receipts
are separate future evidence: neither may infer, replay, or stand in for the
other.

## Failure and rollback

An unavailable forge, missing eligible shared runner, failed hosted job,
candidate mismatch, or absent protection blocks only that platform's
publication. The response is to retain the block and evidence, not to broaden
runtime scope or create a local permanent executor. Reverting this change
returns the claim to the already archived local carrier and removes only this
follow-on planning surface; it does not erase dated receipts.
