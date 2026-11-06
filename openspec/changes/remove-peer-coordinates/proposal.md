## Why

The owner requires that no tracked file or shipped artifact names a peer: no address, host, port,
project path or account namespace. Every peer receives the same files, GitHub's public one included.
`.ethos/release.toml` declares each peer's `forge_repository`, and the GitLab one is the private
address with its port. Two policy tests also carry a private-space literal as their fixture, while
the repository paradigm asks that tracked text name no private-class address.

ETHOS needs neither field. Its review observation reads each peer's web repository from the
clone's own Git configuration when `forge_repository` is absent: the local
`remote.<name>.forgeRepository`, then the remote's URL. This clone holds the key for both peers,
and the GitLab remote is SSH, so the key is what ETHOS reads. ETHOS's planned `peer-resolution`
retires the tracked field for every peer.

## What Changes

- Remove both `forge_repository` lines from `.ethos/release.toml`. Each peer keeps its id, provider,
  role, Git remote, capabilities and CI surface.
- Build the private-space example of the two target-policy tests at run time from its octets, so the
  tracked text names no private literal while the tests prove the same refusal.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion policy and its tests behave as before, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`.ethos/release.toml` and `tests/unit/test_policy_and_staging.py`. One evidence record and its
claim digest wait for ETHOS's `peer-identity-records`, and the two local command fields wait for
`peer-resolution`. Git history keeps the earlier text. `tasks.md` is the sole progress ledger.
