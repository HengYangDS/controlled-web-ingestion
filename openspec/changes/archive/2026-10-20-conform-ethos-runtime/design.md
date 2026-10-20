# Design

## Context

`docs/reference/conventions.md` names the immutable records: archived OpenSpec Changes,
`evidence/`, `docs/evidence/chronicle/`, `docs/history/` and `docs/plans/`. The Prettier ignore
file excludes the same roots, so the formatter leaves them alone. ETHOS reads another carrier: it
exempts archived OpenSpec Changes and the paths that Git attributes mark `linguist-vendored` or
`linguist-generated` from its Markdown layout and authored-name rules.

The skill projections under `.agents/skills/` date from the July governance overlay. No current
ETHOS producer writes or refreshes adopter skill projections, and these route agents to removed
commands and fields.

## Goals / Non-Goals

**Goals:** every proof gate of the bound ETHOS runtime passes, every immutable record keeps its
captured bytes and name under both the formatter and ETHOS, and a contract test keeps the two
exclusions aligned.

**Non-Goals:** changing any record, exempting an authored document from the layout rule, adding a
repository-owned JSON check beside the ETHOS source format gate, or changing ingestion behavior.

## Decisions

- Mark whole roots with `<root>/** linguist-vendored`, mirroring the Prettier ignore file, rather
  than the two documents the runtime reports today: every file under those roots is a record, so no
  later paradigm rule may reach any of them.
- Use `linguist-vendored`, which ETHOS reads as received and the ETHOS introduction film already
  uses for its captured sources. Laying the two documents out with the native repair was rejected:
  it changes captured bytes, and for the publication record it breaks the manifest digest.
- The test takes its roots from the Prettier ignore file's immutable-records block and asks Git for
  each tracked record's attribute, so each tool keeps its native carrier and the test fails as soon
  as the two disagree.
- Retire the skill projections rather than update them to the current contracts. Without a producer
  they are a hand-maintained copy of ETHOS truth that drifts again; `AGENTS.md` and the ETHOS
  command plane remain the agent entry.
- Format JSON through `ethos lane format`, the owner that ETHOS format selection names. The source
  format gate already checks those files on every proof, so the repository's own Prettier gate keeps
  its Markdown and YAML scope instead of repeating that check.

## Risks / Trade-offs

- [Received roots are also exempt from the paradigm's name rules] → A record's name is part of the
  record; renaming it would break its references and digests.
- [GitHub's language statistics skip `evidence/`] → It holds records, not product source.
- [Reformatting changes the bytes of ten JSON files] → Their readers parse JSON, so only whitespace
  changes, and a parse comparison guards each one. The 2026-07-14 publication manifest keeps the
  published digests of two projections as a record of that publication; nothing binds it to the
  current tree, whose files already differ for 43 of its 48 members.
- [Agents lose the skill projections] → They described removed commands and fields; the entry
  document and the installed ETHOS product describe the current ones.
