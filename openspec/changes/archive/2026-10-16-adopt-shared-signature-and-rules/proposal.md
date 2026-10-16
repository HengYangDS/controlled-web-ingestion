## Why

ETHOS now requires an SSH signature and the shared subject grammar on every
commit in every governed repository, and owns that rule in its repository
paradigm. The `signing_required` and `signing_format` fields this repository
declares in `[commit_policy]` are therefore restated declarations, and the
`[[package]]` table in `.ethos/workspace.toml` is a declaration no ETHOS reader
consults. The paradigm also requires OpenSpec configurations to begin their
artifact rules with the common rules. The current runtime reports all three,
and proof blocks until they are repaired.

## What Changes

- Switch the hooks to the ETHOS runtime that holds the shared signature rule.
- Apply `ethos lane repair-paradigm --apply`. It deletes the restated signing
  fields and the `[[package]]` table, removes the emptied
  `.ethos/workspace.toml`, and adds the common OpenSpec rules to
  `openspec/config.yaml`.
- Update the boundary contract test that read the removed binding.
- Align `governance-closeout` with the paradigm. The binding files stay within
  the governing schema, commits carry the paradigm's signature without a
  repository declaration, and the requirement to declare every branch-role
  field is removed.

## Evidence Boundary

Local evidence only: strict OpenSpec validation, the repository gates, the ETHOS
proof in the Work Lane and native signature verification of the new commits.

## Non-goals

- Existing commits are not re-signed or rewritten.
- The hosted pipelines do not run ETHOS, so they need no trust anchor.
