## ADDED Requirements

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
