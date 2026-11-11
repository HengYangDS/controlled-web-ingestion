## Why

The repository runs ETHOS 0.2.0-beta.7 through the family's runtime selection; it tracks no ETHOS
version. The owner asked that every governed repository run the latest ETHOS release.

Its adopter-facing changes since 0.2.0-beta.7 are these:

- The protected-peer feed reads the host, port and namespace path of a remote's `forgeRepository`,
  as its documentation states, instead of only its whole value as a path. The peer's web address on
  its own port in the July governance-closeout record then classifies as a span that
  `ethos lane redact private-addresses` replaces; under 0.2.0-beta.7 the verb refused it as
  unclassified. `redact-peer-addresses` uses it after this Change.
- A governed repository may keep at its root the Markdown community health files that GitHub reads
  there, beside `CONTRIBUTING.md`: `ACCESSIBILITY.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` and
  `SUPPORT.md`. This repository keeps none of them; its root documents stay `AGENTS.md`,
  `CHANGELOG.md`, `CONTRIBUTING.md` and `README.md`.
- `ethos lane repair-paradigm --apply` and the profile that `ethos adopt` writes indent TOML arrays
  by two spaces, as the shipped Taplo policy does, instead of four. This repository's profile
  already holds `record_roots` with that indent since `retire-rules-binding`.
- It upgrades directly from 0.2.0-beta.7 and keeps result schema 3.
- Among its known open defects, Go's GO-2026-6859 affects the bundled `cue`, `vale` and `shfmt`,
  which ETHOS runs only as local commands over repository files without starting an HTTP server.

## What Changes

- Bind the repository family to the 0.2.0-beta.8 runtime, installed with native Mise from the
  release's own declaration, through its console's `hook install`, keeping 0.2.0-beta.7 as the
  rollback.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion policy, its tests and its publication behave as before, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The repository-common runtime selection only. `tasks.md` is the sole progress ledger.
