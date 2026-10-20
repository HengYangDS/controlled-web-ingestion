# Change: Adopt The Markdown Layout Rule

## Why

The ETHOS runtime of `846b529ac` lays out every authored Markdown document by its parsed
structure and exempts received documents, which Git attributes mark `linguist-vendored` or
`linguist-generated`. It reports two documents here:
`docs/plans/2026-07-14-controlled-web-ingestion-topology-implementation.md` and
`evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-implementation.md`. Both are immutable
records. `docs/reference/conventions.md` keeps `evidence/`, `docs/evidence/chronicle/`,
`docs/history/` and `docs/plans/` at their captured bytes, the Prettier ignore file excludes
them, and the 2026-07-14 publication manifest binds the second document's bytes. Nothing tells
ETHOS that these records are not authored, so its repair would rewrite them.

## What Changes

- Mark the four immutable record roots `linguist-vendored` in `.gitattributes`, the attribute
  ETHOS reads as received, so the paradigm leaves their bytes and names as captured.
- State that binding in `docs/reference/conventions.md` beside the formatter exclusion.
- Add a contract test that requires every tracked record under the roots the Prettier ignore
  file excludes as immutable to be `linguist-vendored`, apart from archived OpenSpec Changes,
  which ETHOS already keeps.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`.gitattributes` gains four rules, `docs/reference/conventions.md` one sentence and the contract
tests one test. No record changes bytes, and every authored Markdown document already conforms.
Hosted acceptance of both pipelines follows the landing. `tasks.md` is the sole progress ledger.
