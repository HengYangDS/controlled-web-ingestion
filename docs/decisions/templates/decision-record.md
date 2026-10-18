---
subject: controlled-web-ingestion:decision-record-template
role: template
state: canonical
relations:
  canonical_for: decision record authoring
---

# Decision Record Template

Name a record `dr-NNNN-<topic>.md`, set `decision_id` to `DR-NNNN` and
`decision_status` to `accepted` beside `role` `decision` and `state`
`canonical` in its front matter, and title it `DR-NNNN: <ruling>`. Keep the
rationale in prose; commands, fenced blocks and task lists belong to their
native owners.

## Context

State the evidence and forces that made the decision necessary.

## Decision

State the ruling.

## Alternatives Rejected

Name each material alternative and why it was rejected.

## Consequences and Boundary

State the affected boundaries and the rollback posture.

## Evidence and Revisit

Name the evidence behind the ruling and the condition that reopens it.
