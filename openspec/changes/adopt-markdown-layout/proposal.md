# Change: Adopt The Markdown Layout Rule

## Why

The ETHOS runtime of `846b529ac` lays out every authored Markdown document by its parsed
structure: one blank line between blocks, tight one-block list items and no edge padding. It
reports two documents here. `docs/plans/2026-07-14-controlled-web-ingestion-topology-implementation.md`
is an authored plan. `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-implementation.md` is
a member of the 2026-07-14 publication record, and
`evidence/benchmarks/2026-07-14-publication-manifest.json` binds its exact bytes, so laying it
out would break that record.

## What Changes

- Mark the 2026-07-14 publication record, `evidence/benchmarks/2026-07-14-*`, as received
  through `.gitattributes` with `linguist-vendored`, the attribute ETHOS reads as received, so its
  documents keep their published bytes.
- Lay out the topology implementation plan with `ethos lane repair-paradigm --apply`, which
  changes only its blank lines.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`.gitattributes` gains one rule and the plan's blank lines change; no other tracked byte changes.
Every member of the publication record keeps its manifest digest. Hosted acceptance of both
pipelines follows the landing. `tasks.md` is the sole progress ledger.
