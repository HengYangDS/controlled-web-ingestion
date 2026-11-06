## Context

See [proposal.md](proposal.md). The GitLab peer's address and port appear in shared content through
the release declaration. The target-policy tests use a private-space address as an input, to prove
that a public name that resolves into private space is refused. The loopback controls in the
Firecrawl adapter, runtime, validation and compose projection stay, because loopback leaves the
private-address class in ETHOS's `private-address-class`.

## Goals / Non-Goals

**Goals:**

- No tracked file outside the evidence records names a peer or a private-space literal.
- Publication, review observation and the policy tests keep working.

**Non-Goals:**

- Redacting the evidence record and its claim digest, which waits for ETHOS's redaction verb and
  its digest-follow rule.
- Removing the local command fields, which the installed ETHOS still requires.

## Decisions

- Drop `forge_repository` now. The clone's key holds the same web repository for both peers.
- Join the test's address at run time from its octets. The test still proves the same refusal, and
  the reason string is built from the same value.

## Risks / Trade-offs

- [A clone without the key cannot observe GitLab proposal reviews, because the remote is SSH] →
  ETHOS reports that review state as unknown and names the native `git config` follow-up.

## Migration Plan

Edit the two files, prove the archived head, and publish through the established `dev` and `main`
route. To roll back, revert the commits through a new Change.
