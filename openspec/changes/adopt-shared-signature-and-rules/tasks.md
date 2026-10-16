# Tasks

## 1. Runtime

- [x] 1.1 Switch the hooks to the ETHOS runtime that requires the shared signature with `hook install`; done when `ethos status` reports it current and the repair preview names the restated signature, the `[[package]]` table and the missing common rules. The runtime of ETHOS `471c72ade` installed d0043b95, `ethos status` passes, and the preview names all three.

## 2. Repair

- [x] 2.1 Apply `ethos lane repair-paradigm --apply`; done when `.ethos/workspace.toml` is removed, `openspec/config.yaml` begins its artifact rules with the common rules and the paradigm report has no gap. The repair removed the binding and added the common rules, and the paradigm report is conforming.
- [x] 2.2 Make `tests/contract/test_ethos_boundary.py` assert that the workspace binding is absent; done when the contract tests pass. The four contract tests pass.

## 3. Capability

- [x] 3.1 Align `governance-closeout` with the paradigm-owned signature and branch roles; done when strict OpenSpec validation passes. Strict validation passes.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
