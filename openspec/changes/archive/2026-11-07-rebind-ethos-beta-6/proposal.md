## Why

The repository runs ETHOS 0.2.0-beta.5 through the family's runtime selection; it tracks no ETHOS
version. The owner asked that every governed repository run the latest ETHOS release.
0.2.0-beta.6 retires two fields that this repository's `.ethos/release.toml` declares:
`local_verification_command` and `local_installation_command`. Its loader refuses them, so the move
needs a tracked change as well as the runtime selection.

Its adopter-facing changes since 0.2.0-beta.5 are these:

- **The publication declaration names no command that ETHOS does not run.**
  `ethos lane repair-paradigm --apply` removes the two command fields without echoing their values.
- Review observation resolves a peer's web repository from the clone's local
  `remote.<name>.forgeRepository`, else from an `http` or `https` remote without userinfo. This
  clone holds the key for both peers.
- Result schema 3 bounds large results and gives `next` its final vocabulary.
- A rollback across the repaired declaration refuses until the predecessor's declaration is restored
  in a lane.

## What Changes

- Bind the repository family to the 0.2.0-beta.6 runtime, installed with native Mise from the
  release's own declaration, through its console's `hook install`, keeping 0.2.0-beta.5 as the
  rollback.
- Remove the two retired command fields from `.ethos/release.toml` with the deterministic paradigm
  repair.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion policy, its tests and its publication behave as before, so `.openspec.yaml`
sets `skip_specs: true`.

## Impact

`.ethos/release.toml` and the repository-common runtime selection. `tasks.md` is the sole progress
ledger.
