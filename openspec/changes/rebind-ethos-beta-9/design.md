## Context

See [proposal.md](proposal.md). The move follows ETHOS's successor-first adopter cutover: bind the
release from the lane, prove, then land and publish `dev`, and take `main` through the pull request
and merge request. Between 0.2.0-beta.8 and 0.2.0-beta.9 the embedded OpenSpec moves to 2.0.0 and
the redaction scan is shared; the common CI model is unchanged.

## Goals / Non-Goals

**Goals:**

- Run every gate and lifecycle command of the family on 0.2.0-beta.9.
- Keep the 0.2.0-beta.8 runtime as the rollback until the landing is accepted.

**Non-Goals:**

- Changing any gate, test, CI file or dependency.
- The redaction, which `redact-peer-addresses` does in the same lane after this Change, and the
  0.1.0 release cut, which `cut-release-0-1-0` does after that.

## Decisions

- Install the runtime from the release's own declaration, after checking it against the release's
  `SHA256SUMS` and asset digests, and check the runtime manifest's source commit.

## Risks / Trade-offs

- [A gate that passed under 0.2.0-beta.8 fails under 0.2.0-beta.9] → The lane runs the gates after
  the bind, and the full proof runs at the archived head before landing. A failure is repaired at
  its owner, or the family binds the retained runtime again.

## Migration Plan

Install the runtime, bind it from the lane, run the gates, prove the archived head, land, publish
`dev`, and fast-forward `main` after its review checks pass. To roll back, bind the retained runtime
with the current console's `hook install --runtime <0.2.0-beta.8 runtime>`.
