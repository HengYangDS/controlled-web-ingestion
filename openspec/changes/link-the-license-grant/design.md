## Context

See [proposal.md](proposal.md). ETHOS's paradigm reports `license-entry` until the repository's
public entry links its license grant; the proof preview of `establish-version-identity` reported
that gap after the grant arrived.

## Goals / Non-Goals

**Goals:**

- Link the license grant from the README and declare it in the package metadata.

**Non-Goals:**

- Changing the grant, the version or any behaviour.

## Decisions

- Use the wording the other governed repositories use: the code is licensed under the MIT License.
- Declare the license by its SPDX expression with `license-files`, which Hatchling reads.

## Risks / Trade-offs

- [The package build rejects the license metadata] → The lock, the build and every check run in the
  lane before landing.
