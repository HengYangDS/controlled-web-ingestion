# Design

## Evidence topology

The closeout is a repository artifact, not an operational result cache. It
contains statuses, identifiers, commands, digests and limitations only. It
does not contain pages, HTML, Markdown, raw responses, credentials or private
targets. Historical proof remains historical: a dated receipt may establish its
own bounded fact, but it cannot prove the current work-lane head or current
runner availability.

## Delivery topology

The active Work Lane starts from `candidate/controlled-web-ingestion`; the
candidate is the sole future MR source and `main` remains the protected
publication root. The preceding bootstrap decision established the role
separation. This change adds delivery governance and does not change the
controlled-ingestion runtime, its allowlist, or its persistence model.

## Runner boundary

The current inquiry is observational. A reachable configured workstation runner
is not automatically an eligible repository runner, and an unreachable GitLab
endpoint does not authorize a new personal daemon. Hosted verification remains
pending until GitLab is reachable and schedules an eligible runner for the
actual candidate pipeline.

## Closeout and rollback

The work-lane changes are documents, evidence, an ETHOS profile material-path
binding, and an OpenSpec carrier. They can be reverted as a bounded governance
change. No runtime service, image, Docker setting, persistent store, or runner
registration is introduced, so rollback never requires operational teardown.
