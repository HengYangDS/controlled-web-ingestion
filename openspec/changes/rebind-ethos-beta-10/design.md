## Context

See [proposal.md](proposal.md). The move follows ETHOS's successor-first adopter cutover: bind the
release from the lane, prove, then land and publish `dev`, and take `main` through the pull request
and merge request. Between 0.2.0-beta.9 and 0.2.0-beta.10 four Breaking rules start to block:
Markdown list spacing, the canonical text owner, package docstrings and README index roles; ETHOS's
own Node moves to 26.13.1. The three docs READMEs and the package markers already conform (583c4f9).

## Goals / Non-Goals

**Goals:**

- Run every gate and lifecycle command of the family on 0.2.0-beta.10.
- Keep the 0.2.0-beta.9 runtime as the rollback until the landing is accepted.

**Non-Goals:**

- Changing any gate, test, CI file or dependency.
- The tool and CI-image moves, which the lane's supply Change makes.

## Decisions

- Install the runtime from the release's own declaration, after checking it against the release's
  `SHA256SUMS` and asset digests, and check the runtime manifest's source commit.
- Repair the list spacing with the rule's own function, `canonical_spacing` of the bound runtime, so
  that the change equals what the gate expects. The release's verb, `ethos lane format --apply`,
  cannot do it here: it honors this repository's Prettier ignore, which names `docs/plans/`, while
  the Markdown gate checks every authored Markdown file. The July plan is a record, and the repair
  removes blank lines only. The Prettier ignore stays as it is.
- Put the frozen status in the README's own `Status` section, where a reader and the candidate
  pre-check both find it; the state's definition stays with ETHOS.

## Risks / Trade-offs

- [A gate that passed under 0.2.0-beta.9 fails under 0.2.0-beta.10] → The lane runs the gates after
  the bind, and the full proof runs at the archived head before landing. A failure is repaired at
  its owner, or the family binds the retained runtime again.

## Migration Plan

Install the runtime, bind it from the lane, run the gates, prove the archived head, land, publish
`dev`, and fast-forward `main` after its review checks pass. To roll back, bind the retained runtime
with the current console's `hook install --runtime <0.2.0-beta.9 runtime>`.
