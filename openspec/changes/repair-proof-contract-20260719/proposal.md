# Reproducible proof-contract repair

## Why

The declared local proof gates currently depend on a bare `python` executable,
which is absent on this workstation even though the locked project environment
is available through `python3`. A benchmark fixture also resolves an external
hostname through live DNS, so the full test suite depends on host DNS while the
production admission policy correctly rejects this host's documentation-range
answer.

## What Changes

- Make declared ETHOS proof-gate commands use the portable `python3` runtime
  selector already supported by the repository wrapper.
- Add a contract regression test that keeps the declared proof commands aligned
  with the portable runtime selector.
- Make the Firecrawl benchmark fixture deterministic by patching only the DNS
  socket boundary used by the policy resolver.
- Preserve production public-IP admission and fail-closed behavior unchanged.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `governance-closeout`: local proof-contract verification becomes portable and
  deterministic without altering runtime admission or collection authority;
  subject=controlled-web-ingestion:governance-closeout; reuse=extend;
  change=modify; facet:lifecycle=local-proof;
  facet:surface=proof-contract-and-benchmark-fixture;
  facet:authority=repository-governance.

## Impact

The change affects `.ethos/profile.toml`, its contract test, one benchmark
fixture, and the OpenSpec carrier. It adds no dependency, service, target,
persistence surface, credential handling, MCP integration, or hosted
publication action.

## Out of Scope

- No Firecrawl runtime execution, image, daemon, Docker, allowlist, or data
  handling change.
- No production resolver injection, relaxed IP policy, or network fallback.
- No GitHub, GitLab, or candidate-branch publication action.
