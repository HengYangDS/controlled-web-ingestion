## Context

See [proposal.md](proposal.md). 0.2.0-beta.6 and 0.2.0-beta.5 each refuse the other's publication
declaration, so the move follows ETHOS's successor-first adopter cutover: bind the release from the
lane, repair the declaration there, prove, then land and publish `dev`, and take `main` through the
pull request and merge request.

## Goals / Non-Goals

**Goals:**

- Run every gate and lifecycle command of the family on 0.2.0-beta.6.
- Keep the 0.2.0-beta.5 runtime as the rollback until the landing is accepted.

**Non-Goals:**

- Changing any gate, test, CI file or dependency.
- Redacting the evidence record, which follows ETHOS's `peer-identity-records`.

## Decisions

- Install the runtime from the release's own declaration, after checking it against the release's
  `SHA256SUMS` and asset digests, and check the runtime manifest's source commit.
- Remove the retired fields only through `ethos lane repair-paradigm --apply`, so no value is
  echoed and the repair is the paradigm's own.

## Risks / Trade-offs

- [A gate that passed under 0.2.0-beta.5 fails under 0.2.0-beta.6] → The lane runs the gates after
  the bind and the repair, and the full proof runs at the archived head before landing. A failure
  is repaired at its owner, or the family restores the 0.2.0-beta.5 declaration in a new Change and
  binds the retained runtime.
- [A rollback after the repair] → ETHOS refuses it with `runtime_rollback_declaration_repaired`
  until a lane restores the predecessor's declaration; the release does not qualify that path.

## Migration Plan

Install the runtime, bind it from the lane, repair the declaration, run the gates, prove the
archived head, land, publish `dev`, and fast-forward `main` after its review checks pass. To roll
back, restore the two command fields in a new Change, then bind the retained runtime with the
current console's `hook install --runtime <0.2.0-beta.5 runtime>`.
