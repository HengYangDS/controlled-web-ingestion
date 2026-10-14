## Why

The governed records now follow the ETHOS identity grammar, but an ETHOS proof of this repository
still blocks. The governing release requires each code-correctness axis to name a gate with a
product quality verifier, and the repository-native test and topology gates have none:

- `quality_gate_verifier_missing:behavior:controlled-web-ingestion-tests`;
- `quality_gate_verifier_missing:static-analysis:controlled-web-ingestion-static`.

The product verifiers run the locked pytest with coverage over the committed tests, isolated Ruff
over the authored Python sources and ShellCheck over the shell scripts. The tree did not yet satisfy
them. The dev environment locked no test runner, tooling under `tools/` was not declared as tooling,
and Ruff and ShellCheck reported findings that the repository's own checks do not cover.

The proof gates and both CI planes also reach two of their owner commands through repository shell
scripts. `tools/ci/scripts/with-python-runtime.sh` only sets two uv variables before `uv run`, and
`tools/ci/run_security_checks.sh` only runs one Gitleaks command. The wrappers are POSIX-only and
add nothing that the native tools lack.

ETHOS also cannot publish the repository, because `.ethos/release.toml` declares no publication
topology, and the GitHub repository of the dual-hosted delivery decision did not exist.

## What Changes

- Two provider gates, `controlled-web-ingestion-behavior` and
  `controlled-web-ingestion-code-analysis`, join the proof floor and own the behavior and
  static-analysis axes. The repository-native gates stay in the floor. The topology gate keeps its
  architecture and import-discipline dimensions.
- `tools/**` is declared `ethos-role=tooling`: it is analysed, but it owes no behavior coverage.
- The dev dependency group locks `pytest`, `pytest-cov` and `pytest-reportlog`. The lock gains six
  packages and changes no existing version.
- Python sources take Ruff's format at 100 columns, the shared formatter width of the governed
  repositories. Findings that formatting cannot fix are corrected one by one: exception chaining, an
  explicit `zip` strictness, a specific `assertRaises`, module-level imports in three tooling
  scripts and two ShellCheck findings.
- `.ethos/release.toml` declares GitLab `origin` as the organization collaboration peer and GitHub
  `github` as the public distribution peer, with the documented test and install commands as the
  local verification and installation commands. The public repository
  `HengYangDS/controlled-web-ingestion` now exists. Its `main` starts at the GitLab-published `main`
  (`423bf9552`) and is protected by an active ruleset that requires pull requests, linear history
  and the four hosted checks.
- The proof gates and both CI planes call `uv run --locked` and `gitleaks git` directly. The proof
  gates add `--offline`, matching their declared network policy. Both wrapper scripts are removed,
  and CI keeps its uv cache and environment paths as declared job variables.
- The ETHOS boundary, CI runtime and source topology contract tests follow the new gate and command
  shape.

## Evidence Boundary

Local evidence only: the ETHOS proof in the Work Lane, the repository test, static, schema,
documentation and security gates, and strict OpenSpec validation. The GitHub repository, its base
and its ruleset are platform facts. Hosted CI and protected-main publication on either platform are
not claimed.

## Non-goals

- No change to ingestion behavior, targets, data classes, runtime topology or delivery rules.
- No migration to the common repository paradigm; that follows separately.
- The Firecrawl runtime scripts under `tools/runtime/` stay. Moving their lifecycle into the
  `web-ingest` runtime and native Compose needs a real Firecrawl run as acceptance, so it follows as
  its own Change.
