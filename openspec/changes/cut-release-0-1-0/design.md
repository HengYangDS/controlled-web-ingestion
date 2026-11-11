## Context

See [proposal.md](proposal.md). ETHOS's paradigm keeps `VERSION` as the only version source of a
repository that declares release tags, and `ethos land --release` signs an annotated `v*` tag from
it at the accepted `main`. The GitHub peer's role is `public_distribution`; by the owner's decision
of 8 November 2026 the GitLab peer's address stays out of tracked files.

## Goals / Non-Goals

**Goals:**

- One dated `[0.1.0]` entry that a user can read as the release's notes.

**Non-Goals:**

- Changing ingestion behaviour, checks, CI or dependencies.
- A link that names the GitLab peer.

## Decisions

- History links point at the GitHub peer only: `[0.1.0]` at the release tag and `[Unreleased]` at
  the comparison from `v0.1.0`. A GitLab link would put the peer's address back into a tracked file.
- Keep the notes as `establish-version-identity` wrote them and add only the date. The runtime bind
  and the redaction in this lane change no behaviour a user of 0.1.0 sees, so they get no entry.

## Risks / Trade-offs

- [The tag is signed before the Forges' jobs pass at its commit] → `ethos land --release` runs only
  after `main`'s jobs pass on both Forges at the landed head.
- [A published tag cannot be withdrawn cleanly] → The tag follows the full proof, the landing and
  both Forges' jobs; a defect found later ships as 0.1.1.

## Migration Plan

Land with the lane, publish `dev`, and take `main` through the pull request and the merge request.
After both Forges' jobs pass at `main`, preview
`ethos land --release --expect-head <main> --release-head <main> --tag v0.1.0` (under
`mirror = "accepted_ff"` the closeout has aligned `dev` and `main`, so both coordinates are the
accepted head; `tools/ddwg-lane/release-tag.zsh` renders it), apply it with `--apply --authorize`,
publish the tag to both peers, create the Releases from the `[0.1.0]` notes with
`gh release create v0.1.0 --verify-tag --notes-file` and `glab release create v0.1.0 --notes-file`
under the owner's accounts, as DDWG's v8.0.0 Releases were made, and read both back. To roll back
before the tag, revert the Change.
