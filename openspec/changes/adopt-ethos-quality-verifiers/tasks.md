# Tasks

## 1. Verifiers

- [x] 1.1 Lock `pytest`, `pytest-cov` and `pytest-reportlog` in the dev group and declare `tools/**`
      as tooling; done when the lock adds only those packages and their dependencies.
- [x] 1.2 Format the Python sources at 100 columns and correct the remaining Ruff and ShellCheck
      findings; done when the product static verifier passes.
- [x] 1.3 Add the behavior and code-analysis provider gates to the proof floor and the
      code-correctness map, and update the contract tests; done when the product behavior verifier
      passes.
- [x] 1.4 Replace both CI wrapper scripts with direct `uv run --locked` and `gitleaks git` calls in
      the proof gates and both CI planes; done when no shell script remains under `tools/ci/` and
      every gate passes.

## 2. Publication

- [x] 2.1 Create the public GitHub repository with `main` at the GitLab-published `main` and an
      active protection ruleset; done when the ruleset is active and `main` is `423bf9552`.
- [x] 2.2 Declare the GitLab and GitHub publication peers and the local commands in
      `.ethos/release.toml`; done when the ETHOS publication topology reports both peers and no gap.

## 3. Verification

- [x] 3.1 Run strict OpenSpec validation and the repository test, static, schema, documentation and
      security gates; done when all pass.
