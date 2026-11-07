## Context

See [proposal.md](proposal.md). ETHOS reads a projection declaration from
`.config/checks/ci-projection/policy.toml`. A `cue` projection exports `compiled` from its source in
an isolated directory and compares each provider's YAML with the tracked file. wib's model defines
the `github` and `gitlab` values at its top level, and `tools/ci/project.py` exports each by name.

## Goals / Non-Goals

**Goals:**

- ETHOS's projection check conforms and detects drift in either pipeline.
- The repository's own projection script and gate keep working unchanged.

**Non-Goals:**

- Changing a pipeline, a runner, an image or the `cue` release.
- Adopting ETHOS's common verification model, which this repository's pipelines do not use.

## Decisions

- Use the declaration's `supply` form with the repository's own `.config/mise/config.toml` and
  `.config/mise/mise.lock`, so ETHOS compiles with the locked `cue` 0.17.1 and no common model.
- Alias the provider values with `let`, because a field named `github` inside `compiled.providers`
  would otherwise refer to itself.

## Risks / Trade-offs

- [Two checks of one relation] → ETHOS's check and the repository's gate read the same model and
  must agree; both run in the proof, so a disagreement fails it.

## Migration Plan

Add the declaration and the three model lines, run both checks, prove and land. To roll back,
remove both edits in a new Change; the repository's own gate is unaffected either way.
