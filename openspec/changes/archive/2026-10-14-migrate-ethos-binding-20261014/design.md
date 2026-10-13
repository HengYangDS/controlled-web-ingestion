## Context

The repository was adopted under the July ETHOS contract. The current ETHOS
reads `.ethos/profile.toml` through a strict declaration that forbids unknown
keys and requires the declared proof gates to equal the proof floor. It reads
`[branch_roles]` with `proposal_branch_prefix` in place of
`submit_branch_prefix`.

## Decisions

1. Migrate in place rather than re-adopt. `ethos adopt` only creates a missing
   binding and would replace the reviewed gate declarations.
2. Keep every reviewed value: the release, accepted and candidate branches, the
   `work/` prefix, the `submit/` proposal prefix, the gate commands and the
   OpenSpec material paths.
3. Put all five declared gates in the floor. Dropping the schema, documentation
   and security descriptors instead would stop ETHOS proofs from running
   reviewed gates.
4. ETHOS cannot admit any write before the binding parses, so this one change
   is committed on a plain `work/` branch and fast-forwarded to the candidate
   and accepted trains. Later changes use ETHOS Work Lanes.

## Rollback

Reset the candidate and accepted trains to `a69955d`. The change touches only
the binding, its contract test and this carrier.
