## Context

See [proposal.md](proposal.md). The redaction verb works only inside the effective record roots: the
paradigm's immutable `openspec/changes/archive/` plus the profile's `record_roots`, which holds
`evidence/` since `retire-rules-binding`. On 12 November 2026 a keyless preview of `34536a584` under
the 0.2.0-beta.8 candidate found two occurrences on line 84 of
`evidence/verification/2026-07-15-controlled-web-ingestion-governance-closeout.json`: an
`authority`, the peer's host with its web port, and a separate `port`. The two spans do not
overlap. The verb derives the protected peer from the checkout's local Git configuration, so it
runs in the lane, a worktree of the canonical checkout.

## Goals / Non-Goals

**Goals:**

- No current tracked file names the GitLab peer's host or ports.
- Every redacted occurrence carries a keyed marker that the owner's key verifies.

**Non-Goals:**

- Rewriting published history or any remote ref.
- Turning on `[peer_identity] mode = "required"`, which takes its own decision.
- Changing any other content of the evidence record.

## Decisions

- Read the owner's key from the login Keychain only into `--key-stdin`; it never reaches an
  argument, a log or a file.
- Verify with `--verify --key-stdin --base <base> --head <head>`, which re-derives the head and
  records the `redaction:private-peer` Attestation.

## Risks / Trade-offs

- [The verb meets an occurrence it cannot classify] → Apply refuses and changes nothing; the lane
  stops and the occurrence goes to ETHOS's owner.
- [The keyed marker breaks a consumer of the JSON file] → The marker replaces text inside one
  string value, and the repository's checks and tests run on the lane before landing.

## Migration Plan

Bind ETHOS 0.2.0-beta.8 first, in the same lane. Preview, apply, preview for zero, verify, run the
checks and prove the archived head, land, publish `dev`, and take `main` through the pull request
and merge request. To roll back, revert the lane's commits.
