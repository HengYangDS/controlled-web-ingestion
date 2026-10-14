# Delivery Governance

## Purpose

Delivery governance keeps Controlled Web Ingestion publication reproducible,
evidence-bound, and independent of any unreviewed local execution path.

## Requirements

### Requirement: Delivery governance preserves controlled authority

The repository SHALL preserve its policy, evidence, and protected-publication
boundaries when it changes a hosted delivery projection.

#### Scenario: a hosted delivery change is proposed

- **WHEN** a change introduces or modifies a hosted delivery projection
- **THEN** it identifies the affected repository authority, verification command,
  protection boundary, and evidence limitation
- **AND** it does not widen ingestion targets, data classes, runtime topology,
  persistent storage, or integration surfaces by implication

### Requirement: Hosted delivery planes remain independent and complete

The repository SHALL treat GitHub and GitLab as independent complete repository
and CI/CD planes, and SHALL use repository-owned owner commands through a thin
workflow projection on each platform.

#### Scenario: a candidate is prepared for hosted publication

- **WHEN** a candidate is presented for release
- **THEN** the same reviewed candidate head is pushed to both hosted repositories
- **AND** GitHub Actions and GitLab CI execute their independent required jobs
- **AND** neither platform's result is treated as proof of the other

### Requirement: Protected publication requires current platform evidence

The repository SHALL require current hosted CI and protected-main evidence for
each platform before declaring a dual-hosted implementation release complete.

#### Scenario: one hosted platform is unavailable

- **WHEN** GitHub or GitLab repository, protection, runner, or network state is
  unavailable
- **THEN** the affected publication remains blocked
- **AND** historical evidence, direct pushes, personal runners, and automatic
  cross-platform merges do not substitute for current platform evidence

### Requirement: Delivery projections preserve reviewable text layout

The repository SHALL define a single cross-format text-layout convention for
reviewed source, documentation, and configuration. The convention SHALL use
one blank line between adjacent semantic units, reserve two blank lines for
Python module-level definitions, and prohibit decorative blank lines in JSON
and JSONL.

#### Scenario: tracked documentation or configuration is verified

- **WHEN** repository-owned documentation verification runs
- **THEN** it rejects missing final newlines, trailing whitespace, three or
  more consecutive blank lines, and blank lines in JSON or JSONL
- **AND** it does not mutate serialized evidence or runtime outputs

### Requirement: Local carrier closure preserves outstanding hosted obligations

The repository SHALL archive a completed local delivery carrier before that
carrier reaches a candidate branch. Archiving a local projection carrier SHALL
preserve its proof history but SHALL NOT close either platform's independent
hosted obligations, which remain in the canonical delivery-governance
requirements and publication reference until platform receipts exist.

#### Scenario: local projection evidence is archived before hosted release

- **WHEN** a completed local delivery projection carrier is archived before
  candidate integration
- **THEN** its dated local proof remains available as local evidence
- **AND** GitHub and GitLab publication remain incomplete until each platform
  records its own candidate parity, hosted CI, protection, and protected-main
  evidence
- **AND** no active local closure carrier is promoted to the candidate branch

### Requirement: GitLab CI runs only on the declared project runner pair

The repository SHALL run GitLab CI only on its project-locked docker-executor runner pair on the
dedicated CI host. Ref protection SHALL select the runner, and every job SHALL name a
digest-pinned image. Any other runner, including one in a person's login session, is a personal
runner.

#### Scenario: a protected ref pipeline runs

- **WHEN** a pipeline runs for a protected ref
- **THEN** its jobs carry the `ci-linux-arm64-container-protected` tag
- **AND** only the project's protected runner can take them

#### Scenario: a review pipeline runs

- **WHEN** a pipeline runs for an unprotected ref or a merge request
- **THEN** its jobs carry the `ci-linux-arm64-container` tag

#### Scenario: a job starts

- **WHEN** a GitLab job starts
- **THEN** its image is a digest reference
- **AND** the job runs without privileged mode or the host Docker socket

#### Scenario: a dependency download fails transiently

- **WHEN** a package download in a GitLab Python job times out or cannot resolve its host
- **THEN** uv retries that download inside the same job
- **AND** a failing test is never retried
