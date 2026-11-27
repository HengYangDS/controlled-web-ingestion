## Context

See [proposal.md](proposal.md). The move follows ETHOS's successor-first adopter cutover: bind the
release in the lane, prove, publish for review, land, and publish the accepted head. Between
0.2.0-beta.11 and 0.2.0-beta.12 the release's entry has no Breaking section. What this repository
meets: the commit grammar gains a type; the Vale policy that its `prose` gate runs ignores one more
front-matter field; staged admissions are judged by the staged tree, with one obligation entering as
reporting; and executed proofs keep gate records in the Git-common store. The Ruff and
format-selection policy changes apply to ETHOS's own source only. The release's known defects are
recorded one file each under its `defects/`; re-read them before the lane starts.

## Goals / Non-Goals

**Goals:**

- Run every gate and lifecycle command of the benchmark, locally and in the hosted jobs, on
  0.2.0-beta.12.
- Declare the repository's own gate providers by their catalog IDs, so that neither of its two
  gates draws the legacy-name note.
- Keep the 0.2.0-beta.11 runtime as the rollback until the landing is accepted.

**Non-Goals:**

- Changing any source, test, gate or declared command of the benchmark beyond the two provider
  names and the contract test that asserts them.
- Thawing the repository: it stays frozen, and only its pin floor moves.
- Moving other supply. A supply move is its own Change, after its dependency check.

## Decisions

- Install the release through native Mise from its own declaration and bind it with the console's
  `hook install`. The repository declares no ETHOS tool and keeps none.
- Replace the two legacy provider names with the catalog IDs that ETHOS's own provider catalog maps
  them to (`provider.code-behavior`, `provider.code-static`). Reason: the rollback release,
  0.2.0-beta.11, accepts a catalog ID, and the legacy names resolve only for one support window.
  The gate ids, kinds, dimensions and evidence classes stay as they are.
- Launch every local proof under the lane's own `mise exec`, so a declared command gate finds the
  tools the repository declares. Never launch with the Mise activation state removed alone.
- Record nothing in the Changelog: its entries are the benchmark's releases, and no ETHOS bind of
  this repository has added one.

## Risks / Trade-offs

- [A gate that passed under 0.2.0-beta.11 fails under 0.2.0-beta.12] → The release's proof on a
  disposable copy of this tree passed before the tag. If the lane still meets a failure, it is
  repaired at its owner, or the family binds the retained 0.2.0-beta.11 runtime again.
- [A catalog ID selects another provider than the legacy name did] → The catalog maps each legacy
  name to exactly one ID; the proof after the rename must run both gates with the same results and
  without the note `gate_provider_legacy_name`.
- [The release's journey reports a rollback after the declaration repair as not qualified] → A
  rollback binds the retained runtime and runs the full proof before it lands.

## Migration Plan

Install the release, bind the runtime, rename the providers, run the gates and prove the archived
head; then propose, read both forges' review runs, land and publish. To roll back, bind the retained
runtime from a Work Lane with the current console's
`hook install --runtime <0.2.0-beta.11 runtime> --reason <text>`.
