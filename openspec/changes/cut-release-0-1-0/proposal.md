## Why

The owner decided on 9 November 2026 that Controlled Web Ingestion releases under the MIT License
from 0.1.0, with the tag and the Forges' Releases in its ETHOS binding lane, which since 12 November
2026 also binds 0.2.0-beta.8. `VERSION` has named 0.1.0 since `establish-version-identity`, and
`CHANGELOG.md` keeps the notes under `[Unreleased]`. `redact-peer-addresses`, earlier in this lane,
removes the GitLab peer's address from the current files, so the release's source names no private
address.

## What Changes

- Date the `[Unreleased]` notes as `[0.1.0]`, add history links to the GitHub peer, and open a new
  empty `[Unreleased]`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. This Change edits release notes only, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`CHANGELOG.md` only. The signed `v0.1.0` tag, which `ethos land --release` creates at the landed
`main`, its publication to both peers, and the GitHub and GitLab Releases follow the landed source
and are not tasks of this Change. `tasks.md` is the sole progress ledger.
