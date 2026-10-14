## ADDED Requirements

### Requirement: Governed records follow the ETHOS identity grammar

The repository SHALL name its decision records, archived Change roots and
capability roots in the identity grammar of the ETHOS release that governs it,
and SHALL give every documentation directory with several entries an entrance
that links them.

#### Scenario: ETHOS audits the repository

- **WHEN** the ETHOS repository audit reads the documents and OpenSpec roots
- **THEN** every decision record is named `dr-<positive four-digit id>-<topic>.md`
- **AND** every archived Change root is its archive date and logical identifier
- **AND** every capability root holds only its `spec.md`

#### Scenario: a dated record is renamed

- **WHEN** a record moves to satisfy the identity grammar
- **THEN** its content is unchanged
- **AND** digest-bound evidence that names its earlier path is not rewritten
