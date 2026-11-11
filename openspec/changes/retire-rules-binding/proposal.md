## Why

ETHOS 0.2.0-beta.7, which `rebind-ethos-beta-7` binds earlier in this lane, no longer reads
`.ethos/rules.toml`. Its paradigm repair, planned in every adopter pre-check since 9 November 2026,
moves the evidence directories of that file's `[artifacts]` table into the profile's
`record_roots` and removes the tables that no reader consults.

## What Changes

- Run ETHOS's paradigm repair until it reports no gap. The first run adds
  `record_roots = ["evidence/"]` to `.ethos/profile.toml` and deletes the `[command_plane]`,
  `[formats]` and `[gates]` tables; the second deletes `[artifacts]`, whose roots the profile then
  holds, and with no table left the file goes.
- The governance-closeout specification's binding file set follows.
- `.config/checks/taplo/taplo.toml` takes ETHOS's shipped `[formatting]` and `[schema]` settings,
  keeping its own file selection. ETHOS renders every TOML file with both its shipped policy and
  the repository's, and the repository's Taplo defaults collapse the repaired one-item array that
  the shipped policy keeps open, so the format check refused the repaired profile.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `governance-closeout`: the ETHOS binding file set loses `.ethos/rules.toml`, and the profile's
  `record_roots` names the evidence directory that its `[artifacts]` table held.

## Impact

`.ethos/profile.toml`, `.ethos/rules.toml` (removed), `.config/checks/taplo/taplo.toml` and the
governance-closeout specification. No code, test or workflow reads the removed file, and no other
TOML file changes under the aligned formatter settings. The redaction of the peer address in the
evidence records, which needs these record roots, follows in a later Change. `tasks.md` is the sole
progress ledger.
