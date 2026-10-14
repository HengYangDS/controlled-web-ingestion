## ADDED Requirements

### Requirement: The ETHOS binding holds only runtime-defined files

The repository SHALL keep only the ETHOS binding files whose schemas the governing runtime defines,
and SHALL NOT track ETHOS state.

#### Scenario: ETHOS reports the repository paradigm

- **WHEN** ETHOS audits the binding file set
- **THEN** `.ethos/` holds only `profile.toml`, `workspace.toml`, `release.toml` and `rules.toml`
- **AND** no tracked file declares a state directory under `.ethos/`

### Requirement: Tracked text is normalized to LF

The repository SHALL end `.gitattributes` with the catch-all `* text=auto eol=lf`.

#### Scenario: Git normalizes a text file

- **WHEN** a text file is added without a narrower attribute
- **THEN** Git stores it with LF line endings
