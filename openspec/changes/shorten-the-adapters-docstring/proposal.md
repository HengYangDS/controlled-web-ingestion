# Proposal

## Why

The package docstring that `index-readmes-and-document-packages` gave
`src/web_ingestion/adapters/__init__.py` is 109 characters long, and the code-analysis gate checks
source at 100 columns, so the lane's proof refused it with `E501`.

## What Changes

- Shorten that docstring to one line within 100 columns that still names the package's purpose.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Only a docstring's wording changes, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`src/web_ingestion/adapters/__init__.py` only. `tasks.md` is the sole progress ledger.
