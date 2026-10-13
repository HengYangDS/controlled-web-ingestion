# Tasks

## 1. Binding

- [x] 1.1 Rename `submit_branch_prefix` to `proposal_branch_prefix` with the
  existing value; done when `[branch_roles]` has no unknown field.
- [x] 1.2 Remove the predecessor profile keys and put the five declared gates in
  the proof floor; done when the profile validates under the current ETHOS.
- [x] 1.3 Update the ETHOS boundary contract test; done when it asserts the
  migrated binding.

## 2. Verification and closeout

- [x] 2.1 Run strict OpenSpec validation and the repository test, static,
  schema, documentation and security gates; done when all pass.
- [x] 2.2 Run `ethos status` on the migrated branch; done when the binding
  parses and only the Work Lane lease and hook installation remain.
