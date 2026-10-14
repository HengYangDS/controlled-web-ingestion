## Why

Landing the first ETHOS-governed Change of this repository blocked with `candidate_update_failed`.
ETHOS reads branch roles for ref movement with its strict parser, which requires the complete
`[branch_roles]` table. This repository's table predates two fields, `release_mirror` and
`canonical_sibling_worktrees`. ETHOS therefore fell back to its product default roles and could not
classify the candidate branch.

## What Changes

- `.ethos/workspace.toml` declares `release_mirror = "independent"` and
  `canonical_sibling_worktrees = false`. These are the values the lenient reader already assumed, so
  the roles and their behavior stay the same: `main` remains an independent protected release root,
  and Work Lanes keep their explicit paths.

## Evidence Boundary

Local evidence only: the strict branch-role parse, the ETHOS proof and the landing of this Work
Lane.

## Non-goals

- No change to branch names, the candidate train or the release path.
- The common Work Lane layout with canonical sibling worktrees follows with the repository paradigm
  migration.
