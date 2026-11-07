## Why

The repository renders `.gitlab-ci.yml` and `.github/workflows/verify.yml` from
`.config/ci/pipeline.cue` with its own `tools/ci/project.py`, and its gate
`controlled-web-ingestion-ci-projection` fails on any drift. ETHOS does not know that relation:
`ethos lane project --check` reports `projection_declaration_missing`, so every lane carries that gap
as a known exception, and ETHOS cannot regenerate or check the pipelines itself.

## What Changes

- Declare the projection in `.config/checks/ci-projection/policy.toml` with ETHOS's
  `ethos-ci-template-consistency-v1` schema: both providers are `cue` projections of
  `.config/ci/pipeline.cue`, compiled with the `cue` release that the repository's own Mise
  configuration and lock declare.
- Expose the model's two provider values under `compiled.providers` in `pipeline.cue`, the field that
  ETHOS's compiler reads. The pipelines themselves do not change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The pipelines, their check and the repository's own projection script behave as before, so
`.openspec.yaml` sets `skip_specs: true`.

## Impact

`.config/checks/ci-projection/policy.toml` and `.config/ci/pipeline.cue`. `tasks.md` is the sole
progress ledger.
