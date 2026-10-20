# Tasks

## 1. Received record

- [x] 1.1 Mark `evidence/benchmarks/2026-07-14-*` `linguist-vendored` in `.gitattributes`; done when the repair preview no longer lists the publication record and every member still matches `evidence/benchmarks/2026-07-14-publication-manifest.json`. The preview lists only the plan, and the ten members kept under `evidence/benchmarks/` keep their manifest digests.

## 2. Layout

- [x] 2.1 Lay out `docs/plans/2026-07-14-controlled-web-ingestion-topology-implementation.md` with `ethos lane repair-paradigm --apply`; done when only its blank lines change, the paradigm reports conforming and `mise run check` passes. Its 210 non-blank lines are unchanged, the repair leaves no gap and `mise run check` passes.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published head's GitHub workflow and GitLab pipeline pass.
