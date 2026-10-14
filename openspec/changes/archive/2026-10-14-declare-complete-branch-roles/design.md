## Context

ETHOS admits every ref movement under the branch-role policy that it reads strictly from the
committed `.ethos/workspace.toml`. The strict reader requires all seven fields of `[branch_roles]`.
When neither the incumbent nor the proposed commit carries a complete table, ETHOS falls back to its
product default roles.

## Decisions

1. Declare the two missing fields with the values that the lenient reader already assumed. The
   roles do not move, so no ref, worktree or release path changes.
2. Keep `canonical_sibling_worktrees = false`. The accepted root is the sibling checkout
   `web-ingestion-benchmark-accepted`, so the common Work Lane layout would derive lane paths from
   that name. Adopting the common layout belongs to the repository paradigm migration.

## Rollback

Revert this change. The table returns to its previous five fields, and ETHOS again cannot land a
Work Lane here.
