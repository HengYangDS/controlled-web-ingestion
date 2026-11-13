# Proposal

## Why

ETHOS 0.2.0-beta.10 adds two report-only documentation rules that this repository does not yet meet.
Every README that the docs registry admits declares `role: index`, and every Python package marker
opens with a one-line docstring that names the package's purpose. Three README files under `docs/`
declare another role: `docs/evidence/README.md` (`evidence`), `docs/history/README.md` (`history`)
and `docs/start/README.md` (`how-to`). Six `__init__.py` files are empty. ETHOS's owner decided how
the three README files conform: the evidence and history pages become indexes as they stand, and the
start guide's body moves to a named how-to page. Meeting the rules now keeps the 0.2.0-beta.10
binding a pure binding.

## What Changes

- Declare `role: index` in `docs/evidence/README.md` and `docs/history/README.md`, unchanged
  otherwise.
- Move the body of `docs/start/README.md` to `docs/start/first-run.md` with its subject, role and
  relations, and replace the README with a short index of `first-run.md` and
  `adopter-governance.md`.
- Point the root README's start-guide link at `docs/start/first-run.md`.
- Open each of the six empty package markers with a one-line docstring that names the package's
  purpose.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts and the documentation's content are unchanged, so `.openspec.yaml`
sets `skip_specs: true`.

## Impact

`README.md`, `docs/start/README.md`, the new `docs/start/first-run.md`, `docs/evidence/README.md`,
`docs/history/README.md` and six `__init__.py` files. `tasks.md` is the sole progress ledger.
