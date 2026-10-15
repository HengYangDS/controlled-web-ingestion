## Why

ETHOS holds every governed repository to one repository paradigm. Its current
report finds seven gaps here:

- no Prettier, taplo or Ruff binding under `.config/checks/<tool>/`;
- the `gitlab` publication peer still uses the implicit Git remote `origin`;
- the accepted branch, candidate branch and proposal prefix are not the
  standard `dev`, `candidate/dev` and `proposal/`.

The commit grammar is now also a paradigm value, so the restated
`subject_pattern` becomes a gap once ETHOS reports restated grammars. The hooks
bound an ETHOS runtime that refused write admission, so they moved to the
current runtime before this Change.

## What Changes

- Bind Prettier for Markdown and YAML, taplo for TOML and Ruff for Python with
  the paradigm's settings, excluding immutable records and the ETHOS skill
  projections, and add one proof gate per formatter.
- Format the declared inputs.
- Name the `gitlab` peer's remote `gitlab` and rename the local remote.
- Drop the restated `subject_pattern` so commits use the common grammar.
- Adopt the standard branch roles once ETHOS ships a native migration of the
  role branches; until then the role table, its contract test and the two
  current documents that name the branches stay unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior, contracts and evidence are unchanged, so
`.openspec.yaml` sets `skip_specs: true`.

## Impact

`.config/checks/`, `.ethos/profile.toml`, `.ethos/release.toml`,
`.ethos/workspace.toml`, `docs/reference/conventions.md`, `pyproject.toml` and
the formatted Markdown and YAML documents change. Evidence, archived Changes,
history, chronicle, plans and the skill projections keep their bytes. Remote
branch changes and publication wait for the owner's confirmation.
