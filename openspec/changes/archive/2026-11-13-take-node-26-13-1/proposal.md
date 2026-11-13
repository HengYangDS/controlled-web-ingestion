# Proposal

## Why

Node 26.13.1, published on 10 November 2026, is a security release on the 26 line with nine fixes
rated high under seven CVE identifiers, mostly in its `http2` and `tls` modules, six rated medium
and three rated low. `.config/mise/config.toml` declares node 26.13.0, which runs the repository's
Prettier check locally. The owner's direction is that every supply chain moves to its latest stable
release once it is at least 24 hours old.

## What Changes

- Declare node 26.13.1 in `.config/mise/config.toml` and lock it again with native `mise lock`; only
  node's lock entries change and the lock stays at version 3.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`.config/mise/config.toml` and `.config/mise/mise.lock`. The pipelines install no Mise and keep
their jobs, commands and pins. `main` follows through a pull request on GitHub and a merge request
on GitLab. `tasks.md` is the sole progress ledger.
