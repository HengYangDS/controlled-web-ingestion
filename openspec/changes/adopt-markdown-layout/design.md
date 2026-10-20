# Design

## Context

`docs/reference/conventions.md` names the immutable records: archived OpenSpec Changes,
`evidence/`, `docs/evidence/chronicle/`, `docs/history/` and `docs/plans/`. The Prettier ignore
file excludes the same roots, so the formatter leaves them alone. ETHOS reads another carrier: it
exempts archived OpenSpec Changes and the paths that Git attributes mark `linguist-vendored` or
`linguist-generated` from its Markdown layout and authored-name rules.

## Goals / Non-Goals

**Goals:** every immutable record keeps its captured bytes and name under both the formatter and
ETHOS, and a contract test keeps the two exclusions aligned.

**Non-Goals:** changing any record, or exempting an authored document from the layout rule.

## Decisions

- Mark whole roots with `<root>/** linguist-vendored`, mirroring the Prettier ignore file, rather
  than the two documents the runtime reports today: every file under those roots is a record,
  so no later paradigm rule may reach any of them.
- Use `linguist-vendored`, which ETHOS reads as received and the ETHOS introduction film already
  uses for its captured sources. Laying the two documents out with the native repair was
  rejected: it changes captured bytes, and for the publication record it breaks the manifest
  digest.
- The test takes its roots from the Prettier ignore file's immutable-records block and asks Git
  for each tracked record's attribute, so each tool keeps its native carrier and the test fails
  as soon as the two disagree.

## Risks / Trade-offs

- [Received roots are also exempt from the paradigm's name rules] → A record's name is part of
  the record; renaming it would break its references and digests.
- [GitHub's language statistics skip `evidence/`] → It holds records, not product source.
