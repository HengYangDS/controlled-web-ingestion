## Context

See [proposal.md](proposal.md). ETHOS 0.2.0-beta.7's paradigm repair reports this repository as
`planned` with four repairs: the record binding `record_roots = ["evidence/"]` and the three
`rules.toml` tables `command_plane`, `formats` and `gates`. The record binding works in two phases:
the profile receives every root first, and only then does the next run delete `[artifacts]`.

## Goals / Non-Goals

**Goals:**

- The binding file set holds only files that the governing ETHOS release reads.
- The evidence directories become record roots through ETHOS's own repair, not a hand edit.

**Non-Goals:**

- Redacting the peer address in the evidence records. Beta.7's keyless preview finds its two
  occurrences inside the new roots, but its apply refuses one of them as unclassified until ETHOS
  feeds the `forgeRepository` host and port; that Change follows a release with the fix.
- Changing any code, test, workflow or evidence record.

## Decisions

- Let `ethos lane repair-paradigm --apply` make every edit, so that the declaration and the
  removals are the paradigm's own.
- Update the governance-closeout specification in the same Change, because its binding file set
  names the removed file.
- Make the repository's Taplo settings the shipped ones, not a hand edit of the repaired array.
  ETHOS treats the shipped formatter policy as mandatory and the repository's as an increment
  that must render every file the same way; the repository's file declared only a column width,
  so Taplo's defaults collapsed short arrays where the shipped policy keeps them as written.

## Risks / Trade-offs

- [A reader still consults `.ethos/rules.toml`] → No tracked code, test, workflow or configuration
  names it besides two historical evidence records and this specification, and the repository's
  checks and full proof run on the archived head before landing.

## Migration Plan

Run the repair until the preview reports `conforming`, check that the keyless redaction preview
places both occurrences inside the roots, run the checks and prove the archived head with the other
Changes of this lane. To roll back, revert the lane's commits.
