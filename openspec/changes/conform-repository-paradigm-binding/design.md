## Context

The repository paradigm admits only the binding files that the ETHOS runtime defines schemas for:
`profile.toml`, `workspace.toml`, `release.toml` and `rules.toml`. It also requires every
repository to normalize text to LF through a final catch-all `.gitattributes` pattern.

## Decisions

1. Drop the superseded files instead of folding them. Neither carries a value that the current
   binding lacks: the projection surfaces belong to the runtime, and the project name repeats
   `profile_id`.
2. Remove the `.ethos/state` exception everywhere it is declared. Leaving the generated-artifact
   home or the ignore exception behind would describe a directory that no producer writes.
3. Append the catch-all last, after `tools/** ethos-role=tooling`. The patterns set different
   attributes, so the tooling role is unchanged.

## Rollback

Revert this change. The superseded files return, and the repository again fails the paradigm report
of the ETHOS release that it runs.
