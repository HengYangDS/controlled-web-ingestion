## MODIFIED Requirements

### Requirement: The ETHOS binding follows the governing ETHOS contract

The repository SHALL keep `.ethos/profile.toml`, and any other ETHOS binding
file it declares, within the strict binding schema of the ETHOS release that
governs it, and SHALL name every declared native proof gate in the proof floor.

#### Scenario: current ETHOS reads the binding

- **WHEN** `ethos status` reads the repository binding
- **THEN** the profile and branch roles validate without unknown fields
- **AND** the proof floor names exactly the declared native gates

#### Scenario: delivery roles are preserved

- **WHEN** the binding is migrated to a new ETHOS contract
- **THEN** the release, accepted and candidate branches and the work and
  proposal prefixes keep their reviewed values

### Requirement: Commits follow the shared grammar and carry SSH signatures

Every new commit SHALL follow the shared subject grammar and carry an SSH
signature, as the governing ETHOS repository paradigm requires; the repository
SHALL NOT restate that policy in its binding.

#### Scenario: ETHOS archives a Change

- **WHEN** ETHOS creates the archive commit of a proven Change
- **THEN** the commit carries an SSH signature that verifies against the host trust anchor
- **AND** `ethos publish` accepts the commit as a publication source

#### Scenario: the binding restates no commit policy

- **WHEN** ETHOS audits the repository binding
- **THEN** no `[commit_policy]` declares `signing_required`, `signing_format` or
  `subject_pattern`
- **AND** commit admission still requires the shared grammar and an SSH signature

## REMOVED Requirements

### Requirement: Branch roles are declared completely

**Reason**: The governing ETHOS repository paradigm fixes every branch role name, and the release binding declares the release mirror, so the repository declares no branch-role table.

**Migration**: None; ETHOS applies the standard roles this repository already uses.
