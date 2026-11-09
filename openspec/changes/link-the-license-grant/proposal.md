## Why

`establish-version-identity` added the MIT `LICENSE`, but the README, the repository's public entry,
does not link it, and ETHOS's paradigm asks that it does. The package metadata does not declare the
license either.

## What Changes

- Add a License section to `README.md` that links `LICENSE`.
- Declare `license = "MIT"` and `license-files = ["LICENSE"]` in `pyproject.toml`, as the other
  governed Python repositories do.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`README.md` and `pyproject.toml`. `tasks.md` is the sole progress ledger.
