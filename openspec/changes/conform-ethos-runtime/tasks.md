# Tasks

## 1. Immutable records

- [x] 1.1 Add a contract test that requires every tracked record under the Prettier ignore file's immutable roots, apart from archived OpenSpec Changes, to be `linguist-vendored`; done when it fails before the attribute rules exist. It failed on 21 unmarked records.
- [x] 1.2 Mark `evidence/`, `docs/evidence/chronicle/`, `docs/history/` and `docs/plans/` `linguist-vendored` in `.gitattributes`; done when the test passes, the repair preview reports conforming and no record differs from its captured bytes. The test passes, the preview reports `conforming`, and no record differs from `6964775`.
- [x] 1.3 State the binding in `docs/reference/conventions.md`; done when its formatter section names the attribute beside the Prettier exclusion and `mise run check` passes.

## 2. Current ETHOS checks

- [x] 2.1 Retire the skill projections under `.agents/skills/` with their Prettier ignore and Taplo exclusion entries and their place in `docs/decisions/decision-code-links.md`; done when no tracked file or live document names `.agents/` and the schema and configuration quality gates report no skill gap. Both gates pass on the ETHOS runtime built from `b67d63cc3`.
- [x] 2.2 Format the ten JSON files under `system/` with `ethos lane format --apply`, and state in the conventions that Prettier formats JSON outside the immutable records; done when the source format gate passes and each file parses to its former value. The gate passes on that runtime, and all ten files parse to their former values.
- [x] 2.3 Remove `ethos orient` from `docs/start/adopter-governance.md`; done when the documentation registry gate reports no unknown command example. The gate passes on that runtime.
- [x] 2.4 Spell the product name Taplo as the shared Vale term rule requires in the conventions; done when the prose gate passes. It passes on the ETHOS runtime built from `b67d63cc3`.

## Workflow follow-up

- Bind the repository to an ETHOS runtime that reads the Prettier ignore file at its carrier before the resulting-HEAD proof.
- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
