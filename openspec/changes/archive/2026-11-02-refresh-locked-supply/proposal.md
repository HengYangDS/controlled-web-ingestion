# Proposal

## Why

The owner's direction of 2 November 2026 is that every supply chain moves to its latest stable
release. An audit that day found `uv.lock` behind on packages that its ranges allow, and the
`rabbitmq:4.4.0-alpine` tag resolving to a republished index. The Mise tools, the pinned actions,
the uv images, Redis and the Firecrawl API are current.

The runtime acceptance of that move failed on a fault the move did not cause. At 22:07 that day the
host's `/etc/ssl/cert.pem` lost `AAA Certificate Services` and `emSign ECC Root CA - G3`, through
Homebrew's mitigation of the compromised eMudhra CAs in
[Apple's advisory](https://support.apple.com/en-us/149555). `default_transport` trusted whatever the
host's bundle held, so `https://example.com/`, the static workload, stopped verifying. Whether a
public target verifies should not depend on one host's bundle.

## What Changes

- Refresh `uv.lock` with `uv lock --upgrade`. `requires-python` stays `>=3.12`.
- Verify public fetches against the `certifi` root store that `uv.lock` pins, declare `certifi` as a
  direct dependency, and state the contract in `docs/reference/contracts.md`.
- Record the republished RabbitMQ index digest in `system/supply-chain/firecrawl-provenance.json`
  and pin it in `system/projections/firecrawl-isolated-compose.yaml`, and commit the runtime
  validation record of the moved set under `evidence/verification/`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/` covers delivery governance and closeout, not ingestion. The ingestion
contract lives in `docs/reference/contracts.md`, which states this change, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`uv.lock`, `pyproject.toml`, `src/web_ingestion/transport.py` and its contract test, the contract
and topology documents, the provenance record, the Compose projection and one new evidence record.
A private root that a host trusts no longer reaches this transport; admitted targets are public. The
pipelines keep their jobs, matrix, commands and pins. The design explains what stays: Python 3.15,
the lock rows that upstream ranges hold back, and the Firecrawl API with its companions. Rebinding
the repository to a newer ETHOS runtime is a hook installation, not a file in this Change. `tasks.md`
is the sole progress ledger.
