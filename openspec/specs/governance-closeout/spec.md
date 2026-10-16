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

### Requirement: The ETHOS binding holds only runtime-defined files

The repository SHALL keep only the ETHOS binding files whose schemas the governing runtime defines,
and SHALL NOT track or declare ETHOS state.

#### Scenario: ETHOS reports the repository paradigm

- **WHEN** ETHOS audits the binding file set
- **THEN** `.ethos/` holds only `profile.toml`, `workspace.toml`, `release.toml` and `rules.toml`
- **AND** no tracked file declares a state directory under `.ethos/`
- **AND** `.ethos/rules.toml` declares no state path
- **AND** no tracked copy of ETHOS runtime policy remains under `.config/ethos/`

### Requirement: Tracked text is normalized to LF

The repository SHALL end `.gitattributes` with the catch-all `* text=auto eol=lf`.

#### Scenario: Git normalizes a text file

- **WHEN** a text file is added without a narrower attribute
- **THEN** Git stores it with LF line endings

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

### Requirement: The Firecrawl runtime runs under native Compose and the product lifecycle

The repository SHALL declare the complete Firecrawl topology in its Compose projection with digest
references and healthchecks, and SHALL start, use and remove that topology only through
`web-ingest`, without a repository shell controller.

#### Scenario: a browser request runs the disposable topology

- **WHEN** an admitted browser or crawl request reaches the Firecrawl route
- **THEN** `web-ingest` verifies the reviewed image identities before startup
- **AND** it starts the topology with `docker compose up --wait` and publishes only
  `127.0.0.1:13002`
- **AND** it removes the project with its volumes and verifies that no project resource remains

#### Scenario: a run fails after startup

- **WHEN** the staged request fails while the topology is running
- **THEN** `web-ingest` still removes the project and verifies zero remaining resources
- **AND** the request reports the failure

#### Scenario: the authorized workload set is validated

- **WHEN** an operator runs `web-ingest validate-workloads --evidence PATH`
- **THEN** the reviewed static, browser and crawl workloads, the duplicate, promotion and bridge
  steps, and the service loopback-scrape rejection are checked
- **AND** one body-redacted evidence record is written only after every check passes
