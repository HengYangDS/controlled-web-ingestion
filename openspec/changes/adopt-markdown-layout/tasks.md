# Tasks

## 1. Immutable records

- [x] 1.1 Add a contract test that requires every tracked record under the Prettier ignore file's immutable roots, apart from archived OpenSpec Changes, to be `linguist-vendored`; done when it fails before the attribute rules exist. It failed on 21 unmarked records.
- [x] 1.2 Mark `evidence/`, `docs/evidence/chronicle/`, `docs/history/` and `docs/plans/` `linguist-vendored` in `.gitattributes`; done when the test passes, the repair preview reports conforming and no record differs from its captured bytes. The test passes, the preview reports `conforming`, and no record differs from `6964775`.
- [x] 1.3 State the binding in `docs/reference/conventions.md`; done when its formatter section names the attribute beside the Prettier exclusion and `mise run check` passes.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
