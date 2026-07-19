# Design

## Context

Controlled Web Ingestion keeps production target admission fail-closed and
body-redacted. Its ETHOS adopter profile declares repository-native proof gates
through `with-python-runtime.sh`; this wrapper accepts an interpreter selector
and invokes the locked `uv` environment. The current profile passes `python`,
but the supported local command is `python3`. Separately, the benchmark fixture
uses `https://example.com/`; on this host live DNS resolves it to
`198.18.0.129`, which the production public-IP policy correctly blocks.

## Goals / Non-Goals

**Goals:**

- Make the declared local proof contract execute through the portable runtime
  selector and keep that declaration regression-tested.
- Make the fixture deterministic at its external DNS seam while exercising the
  existing production admission flow.
- Keep the change fully local, body-redacted, and reversible.

**Non-Goals:**

- Altering production DNS, private/public IP admission, target authorization,
  Firecrawl topology, external service state, or hosted delivery.
- Adding a production test hook, configuration option, or resolver override.

## Decisions

### Use `python3` in the declarative proof gates

`python3` is the portable runtime command verified by the existing wrapper.
Using it preserves the wrapper's locked-environment ownership and avoids an
executable alias requirement. Changing the wrapper to search or synthesize a
bare `python` would hide the contract defect and introduce host-specific
resolution policy.

### Patch the fixture's socket boundary, not production APIs

The fixture will patch `web_ingestion.policy.socket.getaddrinfo` to return the
public address `93.184.216.34`. This retains the actual production resolver,
policy, and Firecrawl call path. Adding a resolver parameter to production
`run_firecrawl()` was rejected because it expands the production API solely to
stabilize a test.

### Carry the change as a bounded governance-closeout delta

The existing governance-closeout capability already governs local proof and
evidence boundaries. Its delta records portability and determinism requirements
without creating a runtime capability or confusing local proof with hosted
publication.

## Risks / Trade-offs

- [A new runtime command may be unavailable on a host] -> The regression test
  checks the profile declaration and the native wrapper commands validate the
  selected runtime before proof is claimed.
- [Fixture DNS could conceal policy weakness] -> The patch returns a public IP
  and an explicit production check continues to demonstrate rejection of the
  host's documentation-range DNS result.
- [Planning artifacts could overstate external status] -> This carrier records
  only local proof behavior; GitHub and GitLab remain independent and untouched.

## Migration Plan

1. Add the contract assertion and update the four profile gate selectors.
2. Patch the fixture DNS seam only.
3. Run focused and complete local gates, then the declared ETHOS proof against
   the exact lane head.
4. Commit reviewed lane changes. Reverting the commit restores the former
   declarations and fixture without any runtime teardown.

## Open Questions

None. Hosted publication and candidate integration are separate lifecycle
decisions after local proof.
