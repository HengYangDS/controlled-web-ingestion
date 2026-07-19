## ADDED Requirements

### Requirement: Local proof declarations are portable and deterministic

The repository SHALL declare every Python-based ETHOS proof gate through the
repository runtime wrapper with the portable `python3` selector. Benchmark
fixtures that exercise a policy-resolved public hostname SHALL replace their
external DNS result at the fixture socket boundary with a known public address,
while retaining the production resolver and fail-closed admission policy.

#### Scenario: declared local proof runs on a host without bare python

- **WHEN** the repository executes a Python-based declared proof gate on a host
  where `python` is absent and `python3` is available
- **THEN** the repository wrapper invokes the locked environment using
  `python3`
- **AND** the proof command does not depend on a host-created `python` alias

#### Scenario: benchmark fixture avoids host DNS variability

- **WHEN** the Firecrawl benchmark fixture exercises `https://example.com/`
- **THEN** it supplies a known public DNS answer only at the fixture socket
  boundary
- **AND** the production public-IP admission implementation remains unchanged
- **AND** a documentation-range or non-public answer remains rejected outside
  that fixture patch
