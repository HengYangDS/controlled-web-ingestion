## MODIFIED Requirements

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
