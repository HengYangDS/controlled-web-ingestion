## MODIFIED Requirements

### Requirement: The ETHOS binding holds only runtime-defined files

The repository SHALL keep only the ETHOS binding files whose schemas the governing runtime defines,
and SHALL NOT track or declare ETHOS state.

#### Scenario: ETHOS reports the repository paradigm

- **WHEN** ETHOS audits the binding file set
- **THEN** `.ethos/` holds only `profile.toml`, `workspace.toml`, `release.toml` and `rules.toml`
- **AND** no tracked file declares a state directory under `.ethos/`
- **AND** `.ethos/rules.toml` declares no state path
- **AND** no tracked copy of ETHOS runtime policy remains under `.config/ethos/`
