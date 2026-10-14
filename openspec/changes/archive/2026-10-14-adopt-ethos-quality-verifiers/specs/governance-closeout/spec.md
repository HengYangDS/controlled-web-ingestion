## ADDED Requirements

### Requirement: Product verifiers prove the code-correctness axes

The repository SHALL bind the behavior and static-analysis axes of its ETHOS proof to gates that
carry the product quality verifiers of the governing ETHOS release, and SHALL keep its
repository-native gates in the proof floor.

#### Scenario: ETHOS proves the repository

- **WHEN** an ETHOS proof runs the code-correctness gates
- **THEN** the behavior verifier runs the locked pytest over the committed tests with coverage of
  the product source
- **AND** the static verifier analyses the authored Python and shell sources
- **AND** the repository-native test, topology, schema, documentation and security gates still run

#### Scenario: a test executes a tooling script

- **WHEN** a test executes a committed script under `tools/`
- **THEN** the static verifier analyses the script as tooling
- **AND** the script owes no behavior coverage

### Requirement: Owner commands run without repository shell wrappers

The repository SHALL invoke the owner commands of its proof gates and hosted CI planes through the
native `uv` and `gitleaks` command lines, without a repository shell wrapper.

#### Scenario: a gate or CI job runs an owner command

- **WHEN** a proof gate or a hosted CI job runs a test, schema, documentation, topology or security
  check
- **THEN** it calls `uv run --locked` or `gitleaks git` directly
- **AND** no shell script under `tools/ci/` takes part

### Requirement: ETHOS publication names existing hosted repositories

The repository SHALL declare each existing hosted repository as an ETHOS publication peer, together
with its repository-owned local verification and installation commands.

#### Scenario: ETHOS reads the publication topology

- **WHEN** ETHOS compiles the publication declaration
- **THEN** GitLab `origin` is the organization collaboration peer
- **AND** GitHub `github` is the public distribution peer
- **AND** the topology reports no declaration gap
