## ADDED Requirements

### Requirement: Commits follow the shared grammar and carry SSH signatures

The repository SHALL declare an ETHOS commit policy that requires the shared subject grammar and
an SSH signature on every new commit.

#### Scenario: ETHOS archives a Change

- **WHEN** ETHOS creates the archive commit of a proven Change
- **THEN** the commit carries an SSH signature that verifies against the host trust anchor
- **AND** `ethos publish` accepts the commit as a publication source
