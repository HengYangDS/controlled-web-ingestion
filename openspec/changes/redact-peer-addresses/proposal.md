## Why

The owner decided on 8 November 2026 that the GitLab peer's address leaves the current tracked
files, while published history stays as it is. One tracked file still names it: the governance
closeout evidence of 15 July 2026, at one line with the peer's host and web port and one of its
ports. `ethos lane redact private-addresses` replaces each occurrence inside the effective record
roots with a keyed marker that only the owner's key can verify; since `retire-rules-binding` the
profile's `record_roots` holds `evidence/`, so the record lies inside them. 0.2.0-beta.7 refused
that line as unclassified, because its peer feed read the remote's `forgeRepository` only as a
path; 0.2.0-beta.8, which `rebind-ethos-beta-8` binds in this lane, classifies both occurrences.

## What Changes

- Redact the two occurrences on that line with the owner's key, and verify the redaction.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion policy, its tests and its publication behave as before, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`evidence/verification/2026-07-15-controlled-web-ingestion-governance-closeout.json`, and the sha256
that `evidence/claims/controlled-web-ingestion-governance-closeout-20260715.toml` keeps for it,
which the redaction verb updates with the record. No commit is rewritten, and the remotes keep their
history. `main` follows through a pull request on GitHub and a merge request on GitLab. `tasks.md`
is the sole progress ledger.
