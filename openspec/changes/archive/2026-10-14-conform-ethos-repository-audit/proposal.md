## Why

With the binding migrated, the current ETHOS still cannot run a Work Lane or a
proof here. Its repository audit rejects records that predate its identity
grammar:

- three archived Change roots start with a date or end in a temporal suffix
  (`openspec_change_root_invalid`);
- both capability roots carry a `capability.toml` that ETHOS no longer reads
  (`openspec_spec_capability_entry_unexpected`);
- the four decision records are not named `dr-<positive id>-<topic>.md`, and one
  uses the reserved number 0000 (`docs_decision_name_invalid`);
- five M1–M5 experiment records under `docs/history/` have no document metadata;
- two chronicle directories have no entrance, and two decision READMEs have no
  children.

## What Changes

- Archived Change roots take their logical identifier; the files are unchanged.
- The two `capability.toml` files are removed. Their boundary rules already
  live in the capability specs and in decisions 0002 and 0003.
- Decision records are renamed `dr-0001` to `dr-0003`; the position record,
  formerly 0000, takes the next unused number, 0004.
- The M1–M5 experiment records move byte for byte to `evidence/benchmarks/`,
  beside the receipts of the same experiment.
- The chronicle gains two index READMEs, and the empty `accepted/` and
  `superseded/` decision groupings are removed.
- References, the evolution ledger, two claim pointers and the ETHOS boundary
  contract test follow the new paths.

## Evidence Boundary

Local evidence only: the repository test, static, schema, documentation and
security gates, strict OpenSpec validation and the ETHOS repository audit.
GitLab is unreachable, so hosted CI and publication remain blocked.

## Non-goals

- No change to a decision, requirement, runtime, target or delivery rule.
- The digest-bound verification record of 2026-07-15 and the publication
  manifest of 2026-07-14 keep the paths they observed.
