# Design

## Context

ETHOS reports a `markdown-layout` gap for each authored Markdown document whose blank lines
differ from its parsed structure, and exempts paths that Git attributes mark
`linguist-vendored` or `linguist-generated`. The 2026-07-14 publication record under
`evidence/benchmarks/` is a fixed bundle: its manifest records the digest and size of each
member, including four Markdown documents. The repository's rules name `evidence` a durable
evidence root.

## Goals / Non-Goals

**Goals:** conform every authored document to the layout rule and keep every member of the
publication record byte-identical to its manifest.

**Non-Goals:** rewriting or re-recording the publication record, or changing any other
document.

## Decisions

- Mark the whole bundle, `evidence/benchmarks/2026-07-14-*`, rather than the one document the
  runtime reports today. Every member is fixed by the same manifest, so a later rule must not
  reach any of them; the pattern names the bundle by its publication date.
- Use `linguist-vendored`, the attribute ETHOS already reads as received and that the ETHOS
  introduction film uses for its captured sources. Re-binding the manifest to laid-out bytes was
  rejected: the manifest records what was published.
- Let the native repair lay out the plan, so its result equals the formatter's layout.

## Risks / Trade-offs

- [The attribute also exempts the bundle's names from the authored-name rule] → Its names already
  conform, and any later rename would itself break the manifest.
- [GitHub's language statistics skip the bundle] → It holds records, not product source.
