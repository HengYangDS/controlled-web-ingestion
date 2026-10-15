# Tasks

## 1. Runtime

- [x] 1.1 Switch the hooks to the current ETHOS runtime with `hook install`; done when `ethos status` reports it current. Runtime 9b2bd41f refused write admission as `runtime_build_stale`; the runtime of ETHOS `b8e0d3ce5` installed 7ee760d5 in this repository's Git store, and `ethos status` passes.

## 2. Formatters

- [x] 2.1 Bind Prettier, taplo and Ruff under `.config/checks/<tool>/` with the paradigm settings and the protected-root exclusions; done when the paradigm report has no formatter-binding gap. The three carriers hold the paradigm settings; Prettier leaves embedded code untouched and Ruff checks only Python files. The report's only gaps are the three branch roles.
- [x] 2.2 Add one proof gate per formatter and record the check and fix commands in `docs/reference/conventions.md`; done when the three gates pass. The three commands pass from the lane root.
- [x] 2.3 Format the declared inputs; done when a second pass changes nothing and every excluded file is byte-identical. Prettier rewrote tables, emphasis and YAML comment spacing in five documents, taplo rewrote the arrays of `pyproject.toml`, and Ruff found its 41 files formatted; a second pass changes nothing and no excluded root changed.

## 3. Remote And Commit Grammar

- [x] 3.1 Name the `gitlab` peer's remote `gitlab` in `.ethos/release.toml` and run `git remote rename origin gitlab`; done when the paradigm report has no peer-remote gap and `git remote` lists `gitlab` and `github`. `74be74c` names the remote in the binding, and the rename ran after `40bdb83` landed; `git remote` lists `github` and `gitlab`.
- [x] 3.2 Drop the restated `subject_pattern` and keep the signing settings; done when commit admission accepts the next commit under the derived grammar. This commit is admitted under the derived grammar.

## 4. Branch Roles

- [x] 4.1 Adopt `dev`, `candidate/dev` and `proposal/` in `.ethos/workspace.toml`, `tests/contract/test_ethos_boundary.py` and the current branch names in `docs/decisions/dr-0002-delivery-train-boundary.md` and `docs/start/adopter-governance.md`; done when the role refs carry the standard names and the paradigm report has no gap. ETHOS `39fed382a` ships the native role migration: accepted closeout renamed both refs at `afc677c` and rebound the accepted and candidate worktrees. This commit removes `[branch_roles]`, whose remaining values equal the paradigm defaults.
- [ ] 4.2 Rename the hosted role branches and publish; done when both peers serve `dev` and `main` at the accepted and release heads and no old role branch remains. Both peers serve `dev` at `40bdb83` and `main` at `afc677c`. Blocked, owner ETHOS role migration: both peers still hold `accepted/controlled-web-ingestion` at `afc677c`, and ETHOS admits remote retirement only for proposal refs (`proposal_retirement_target_not_proposal`). Exit when `ethos publish --retire` admits a renamed legacy role ref; review on 2026-10-17.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
