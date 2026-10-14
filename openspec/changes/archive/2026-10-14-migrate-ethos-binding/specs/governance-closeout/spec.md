## ADDED Requirements

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
