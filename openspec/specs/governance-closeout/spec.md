# Governance Closeout

## Purpose

Governance closeout keeps controlled-ingestion evidence, delivery readiness,
and future admission decisions auditable without broadening the runtime,
persistence, target, or integration authority boundary.
## Requirements
### Requirement: Closeout records evidence classes independently

The repository SHALL record topology closeout as body-redacted evidence, shall
distinguish local proof, explicit runtime proof, ETHOS proof, hosted CI,
protected-main publication, and current runner availability, and shall retain
an explicit external block when current hosted verification cannot run.

#### Scenario: evidence is not projected beyond its verifier

- **WHEN** a closeout references a verification result
- **THEN** it names the verifier, commit or timestamp where available, and its
  limit rather than treating a different evidence class as equivalent

#### Scenario: hosted verification is unavailable

- **WHEN** the configured GitLab endpoint or eligible runner cannot be observed
- **THEN** the closeout records a blocked hosted-publication state and does not
  treat historical pipeline or runner evidence as current capacity
### Requirement: New admission remains explicit

The repository SHALL require a new policy, schema, runtime, and evidence review
before any new target, data class, runtime topology, or delivery sink is used.

#### Scenario: a proposed target is outside the reviewed workload

- **WHEN** a requester proposes a target absent from the authorized workload
- **THEN** the repository treats it as a new admission packet and does not reuse
  the published Firecrawl validation as authorization
