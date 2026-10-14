## Context

ETHOS audits a governed repository's documents and OpenSpec roots before it
starts a Work Lane, proves or publishes. The audit grammar tightened after this
repository's July adoption: decision identities are positive four-digit numbers
behind a `dr-` prefix, a Change identifier is a logical name without a date,
and a capability root holds only `spec.md`.

## Decisions

1. Rename rather than rewrite. Every moved file keeps its bytes, so the
   publication manifest digests of the five M1–M5 records still match.
2. Keep decision numbers 0001 to 0003. Only the position record changes,
   because 0000 is not a valid identity; it takes 0004 and says so.
3. Move the M1–M5 records to `evidence/benchmarks/` instead of adding metadata
   to them. They are evidence of the admission experiment, and adding front
   matter would change digest-bound bytes.
4. Remove the two empty decision groupings instead of filling them. The
   decision index already lists every record.
5. Leave dated evidence untouched where it records an observed path.

## Rollback

Revert this change. Nothing outside tracked documents, OpenSpec roots, two
claim pointers and one contract test is touched.
