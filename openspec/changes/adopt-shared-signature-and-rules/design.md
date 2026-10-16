# Design

## Context

`.ethos/workspace.toml` declares one root `[[package]]` and a `[commit_policy]`
with `signing_required = true` and `signing_format = "ssh"`. The ETHOS runtime
that ships tasks 2.24 and 2.25 of its repository paradigm reads neither. It fixes
the branch roles, requires an SSH signature on every governed commit and reports
both tables as restated or unread. The `governance-closeout` capability still
says the repository declares the commit policy and every branch-role field,
which the paradigm now owns.

## Goals / Non-Goals

**Goals:** remove the restated binding with the native repair, add the common
OpenSpec rules, keep the boundary test and the capability true to the binding,
and move to the runtime that requires them in one batch.

**Non-Goals:** changing ingestion behavior, the Firecrawl runtime, any gate or
the signing setup, which already signs every commit with the local SSH signer.

## Decisions

- Use `ethos lane repair-paradigm --apply` after exact-path prewrite admission.
  It removes the emptied binding and keeps every comment in
  `openspec/config.yaml`.
- `.ethos/workspace.toml` stays in the OpenSpec material paths, so a binding
  declared later still needs a Change.
- The boundary test asserts that the binding is absent instead of reading it.

## Risks / Trade-offs

- None for behavior: the runtime already enforces the signature and grammar that
  the removed fields declared.
