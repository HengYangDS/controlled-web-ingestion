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

### Requirement: Local proof declarations are portable and deterministic

The repository SHALL declare every Python-based ETHOS proof gate through the
repository runtime wrapper with the portable `python3` selector. Benchmark
fixtures that exercise a policy-resolved public hostname SHALL replace their
external DNS result at the fixture socket boundary with a known public address,
while retaining the production resolver and fail-closed admission policy.

#### Scenario: declared local proof runs on a host without bare python

- **WHEN** the repository executes a Python-based declared proof gate on a host
  where `python` is absent and `python3` is available
- **THEN** the repository wrapper invokes the locked environment using
  `python3`
- **AND** the proof command does not depend on a host-created `python` alias

#### Scenario: benchmark fixture avoids host DNS variability

- **WHEN** the Firecrawl benchmark fixture exercises `https://example.com/`
- **THEN** it supplies a known public DNS answer only at the fixture socket
  boundary
- **AND** the production public-IP admission implementation remains unchanged
- **AND** a documentation-range or non-public answer remains rejected outside
  that fixture patch

### Requirement: The ETHOS binding follows the governing ETHOS contract

The repository SHALL keep `.ethos/profile.toml` and `.ethos/workspace.toml`
within the strict binding schema of the ETHOS release that governs it, and
SHALL name every declared native proof gate in the proof floor.

#### Scenario: current ETHOS reads the binding

- **WHEN** `ethos status` reads the repository binding
- **THEN** the profile and branch roles validate without unknown fields
- **AND** the proof floor names exactly the declared native gates

#### Scenario: delivery roles are preserved

- **WHEN** the binding is migrated to a new ETHOS contract
- **THEN** the release, accepted and candidate branches and the work and
  proposal prefixes keep their reviewed values
