## Why

`ethos status` no longer reads this repository. ETHOS renamed `[branch_roles]
submit_branch_prefix` to `proposal_branch_prefix` and moved the repository
binding to a strict schema. The July binding therefore fails with
`branch_roles contains unknown fields` and, once that is fixed, with
`repository_profile_invalid:.ethos/profile.toml`. No ETHOS command can admit a
change here until the binding is migrated, and `ethos adopt` refuses to
overwrite an existing profile.

## What Changes

- `.ethos/workspace.toml` names its proposal branches with
  `proposal_branch_prefix`, keeping the existing `submit/` value.
- `.ethos/profile.toml` drops the predecessor schema keys `schema_version`,
  `profile_version`, `ethos_contract_version`, `[repository]` and `[roots]`.
  Its roots already equal the ETHOS defaults.
- The proof floor names all five declared native gates, because the current
  contract requires the declared gates to equal the floor.
- The ETHOS boundary contract test asserts the migrated binding.

## Evidence Boundary

Local evidence only: the repository test, static, schema, documentation and
security gates, strict OpenSpec validation and `ethos status` on this lane.
GitLab is unreachable, so hosted CI and publication remain blocked.

## Non-goals

- No runtime, target, persistence, Firecrawl or delivery-role change.
- No release to `main`. It keeps the July binding until the accepted train is
  released.
