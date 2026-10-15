# Tasks

## 1. Runtime

- [x] 1.1 Switch the hooks to the current ETHOS runtime with `hook install`; done when `ethos status` reports it current. Runtime 9b2bd41f refused write admission as `runtime_build_stale`; the runtime of ETHOS `b8e0d3ce5` installed 7ee760d5 in this repository's Git store, and `ethos status` passes.

## 2. Formatters

- [ ] 2.1 Bind Prettier, taplo and Ruff under `.config/checks/<tool>/` with the paradigm settings and the protected-root exclusions; done when the paradigm report has no formatter-binding gap.
- [ ] 2.2 Add one proof gate per formatter and record the check and fix commands in `docs/reference/conventions.md`; done when the three gates pass.
- [ ] 2.3 Format the declared inputs; done when a second pass changes nothing and every excluded file is byte-identical.

## 3. Remote And Commit Grammar

- [ ] 3.1 Name the `gitlab` peer's remote `gitlab` in `.ethos/release.toml` and run `git remote rename origin gitlab`; done when the paradigm report has no peer-remote gap and `git remote` lists `gitlab` and `github`.
- [ ] 3.2 Drop the restated `subject_pattern` and keep the signing settings; done when commit admission accepts the next commit under the derived grammar.

## 4. Branch Roles

- [ ] 4.1 Adopt `dev`, `candidate/dev` and `proposal/` in `.ethos/workspace.toml`, `tests/contract/test_ethos_boundary.py` and the current branch names in `docs/decisions/dr-0002-delivery-train-boundary.md` and `docs/start/adopter-governance.md`; done when the role refs carry the standard names and the paradigm report has no gap. Blocked, owner ETHOS: no admitted path renames the accepted and candidate refs. Exit when ETHOS ships its native role migration.
- [ ] 4.2 Rename the hosted role branches and publish; done when both peers serve `dev` and `main` at the accepted and release heads and no old role branch remains. Blocked on 4.1 and the owner's confirmation of the remote effects.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
