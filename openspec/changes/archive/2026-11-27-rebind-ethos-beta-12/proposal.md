## Why

The repository declares and runs ETHOS 0.2.0-beta.11. The owner asked that every governed repository
run the latest ETHOS release. 0.2.0-beta.12 upgrades directly from 0.2.0-beta.11 and publishes its
own Mise declaration; the lane checks each of its platform checksums against the release's
`SHA256SUMS` and the published asset digests before using it. The repository is frozen; it takes the
bind and the two steps the bind completes.

What 0.2.0-beta.12 changes that bears on this repository (a selection; the release's entry is the
full list):

- The commit grammar admits the type `style`: the paradigm's types become the eleven that the
  Conventional Commits 1.0.0 configuration names. The repository restates no `subject_pattern`, so
  the paradigm's grammar admits the type once the release is bound.
- A staged admission, the index-target preview of `ethos lane prewrite` and the commit, is judged
  by its staged tree; the obligation `staged-openspec-tree` enters as reporting, so a staged tree
  that does not pass is reported under `reported_gaps` and the working files decide as before.
- An executed proof with a frozen source records each gate's run under `gate-results/` in the
  Git-common store and compares it with earlier runs of the same input; no verdict, gap or
  Attestation changes.
- The shipped Vale policy, which the `prose` gate runs, ignores the front-matter field
  `workaround`; it adds no diagnostic.
- The shipped Docs Registry gains the section "Decision records", which states one form for every
  governed repository's decision records and leaves the move to each repository's own lane. No
  command, schema or check changes with it. This Change does not move the records: the repository
  is frozen, and the freeze admits only the bind.
- Before the tag, the release's candidate was proved on disposable copies of the governed trees. A
  full proof of this repository's tree of that day passed, and proof previews of its later head
  under the release added no required gap and no refusal against 0.2.0-beta.11.

The rebind of 0.2.0-beta.11 left one step to this one: the two gates of `.ethos/profile.toml` name
their providers by legacy `ethos.<module>:<callable>` names, which resolve for one support window
and draw the note `gate_provider_legacy_name` in each proof. 0.2.0-beta.10 refused a catalog ID, so
the names stayed while it was the rollback; the rollback is now 0.2.0-beta.11, which accepts
catalog IDs.

## What Changes

- Bind the repository family to the 0.2.0-beta.12 runtime, installed with native Mise from the
  release's own declaration, through its console's `hook install`, keeping 0.2.0-beta.11 as the
  rollback; the repository declares no ETHOS tool in its Mise configuration and keeps none.
- Name each gate's provider by its catalog ID in `.ethos/profile.toml`: `provider.code-behavior`
  for the behavior gate and `provider.code-static` for the code-analysis gate, and update the
  contract test that asserts the two names.
- Name 0.2.0-beta.12 as the pin floor in the README's frozen status, and correct its sentence that
  the repository takes no further ETHOS bind: the binds of 0.2.0-beta.11 and of this release
  contradict it. The repository stays frozen for supply.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion policy, its tests and its publication behave as before, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The repository-common runtime selection, `.ethos/profile.toml`,
`tests/contract/test_ethos_boundary.py` and `README.md`. `tasks.md` is the
sole progress ledger.
