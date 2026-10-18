# Tasks

## 1. Runtime

- [x] 1.1 Switch the hooks to the current ETHOS runtime with `hook install`; done when `ethos status` reports it current and the repair preview names the toolchain owner, the pipeline model and the two GitHub steps. The runtime of ETHOS `226f746a6` is current, and the preview names `toolchain-owner`, `pipeline-model` and the `python-contracts` and `security` steps.

## 2. Toolchain owner

- [x] 2.1 Add `.config/mise/config.toml` with locked resolution, the tools and the `bootstrap`, `check` and `fix` tasks, and track the lock that `mise lock` writes; done when `mise run bootstrap` installs from the lock and `mise run check` passes. Both pass in the lane, and `mise run fix` changes no tracked file.

## 3. CI model

- [x] 3.1 Model both pipelines in `.config/ci/pipeline.cue`, render them with `tools/ci/project.py`, add the `controlled-web-ingestion-ci-projection` gate and run each GitHub step as one native command; done when `--check` passes, the contract tests pass on the generated files and the paradigm report is conforming. All three hold, and the repair preview reports `conforming`.

## 4. Decision records

- [x] 4.1 Restate `dr-0001` to `dr-0004` and the decision template in the shared decision grammar; done when proof reports no `docs_decision_*` gap. The runtime's decision grammar reports no gap on the restated records.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline run the generated projections.
