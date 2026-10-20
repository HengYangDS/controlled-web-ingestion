# Change: Conform To The ETHOS Runtime

## Why

Binding this repository to the ETHOS runtime built from `846b529ac` adds checks that the current
tree fails:

- The repository paradigm lays out authored Markdown by its parsed structure and exempts received
  documents, which Git attributes mark `linguist-vendored` or `linguist-generated`. It reports two
  immutable records: `docs/plans/2026-07-14-controlled-web-ingestion-topology-implementation.md`
  and `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-implementation.md`.
  `docs/reference/conventions.md` keeps `evidence/`, `docs/evidence/chronicle/`, `docs/history/`
  and `docs/plans/` at their captured bytes, and the 2026-07-14 publication manifest binds the
  second document's bytes, yet nothing tells ETHOS that these records are not authored.
- The schema gate validates the skill projections under `.agents/skills/` against the current
  package, registry and activation contracts and reports 13 findings in the July projections.
  Current ETHOS adoption writes only `.ethos/profile.toml` and `openspec/config.yaml`.
- ETHOS format selection assigns JSON to Prettier. Ten JSON files under `system/` differ from its
  output, while `docs/reference/conventions.md` says that JSON is not formatted.
- `docs/start/adopter-governance.md` still shows `ethos orient`, which the ETHOS command plane no
  longer has.
- The prose gate now also runs the shared Vale policy, whose term rule reports the product name
  Taplo written in lowercase in the conventions.

ETHOS itself read only a root `.prettierignore`, so the records that
`.config/checks/prettier/prettierignore` excludes reported format drift. That defect is fixed in
ETHOS, not here.

## What Changes

- Mark the four immutable record roots `linguist-vendored` in `.gitattributes`, the attribute ETHOS
  reads as received, so the paradigm leaves their bytes and names as captured, and state that
  binding in `docs/reference/conventions.md`.
- Add a contract test that requires every tracked record under the roots the Prettier ignore file
  excludes as immutable to be `linguist-vendored`, apart from archived OpenSpec Changes, which ETHOS
  already keeps.
- Retire the skill projections under `.agents/skills/`, with their Prettier ignore and Taplo
  exclusion entries and their place in the ETHOS boundary of `docs/decisions/decision-code-links.md`.
- Format the ten JSON files with the ETHOS-native Prettier formatter, and state in the
  conventions that Prettier formats JSON outside the immutable records.
- Remove `ethos orient` from the adopter guide.
- Spell the product name Taplo as the shared Vale term rule requires.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`.gitattributes` gains four rules and the contract tests one test. Eight files under
`.agents/skills/` are removed. The ten JSON files change whitespace only and parse to the same
values. The two `system/` JSON files whose digests the 2026-10-14 runtime validation binds already
conform and keep their bytes. The 2026-07-14 publication manifest records the published bytes of
`system/projections/routing.json` and `system/projections/framework-comparison-cases.json`; it
stays a record of that publication, and 43 of its 48 members already differ from or are absent in
the current tree. No immutable record changes bytes. Binding the ETHOS runtime is a local hook
installation, not a tracked change. Changing ingestion behavior, the ETHOS runtime or any immutable
record is out of scope. Hosted acceptance of both pipelines follows the landing. `tasks.md` is the
sole progress ledger.
