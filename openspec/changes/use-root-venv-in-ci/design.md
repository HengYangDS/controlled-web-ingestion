# Design

## Context

`.config/ci/pipeline.cue` owns both pipelines, and `tools/ci/project.py` renders
`.github/workflows/verify.yml` and `.gitlab-ci.yml` from it. The GitHub job runs one Python version
per matrix entry on its own runner; each GitLab job runs one version in its own uv image. Every
check runs as `uv run --locked --python <python> python <check>`. With `UV_PROJECT_ENVIRONMENT`
unset, uv uses the `.venv` directory at the project root, which is where local commands already
run.

## Goals / Non-Goals

**Goals:**

- Run the CI checks in the root `.venv`, the one project environment that the ETHOS
  generated-artifact topology allows.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, caches or pins.

## Decisions

### uv's default project environment replaces the per-version directory

The per-version path kept one environment for each Python version apart, but no job runs more than
one version, so the separation never applied inside a job. uv already places the environment at the
project root when the variable is unset, so removing the variable is the whole change; an explicit
`UV_PROJECT_ENVIRONMENT: .venv` would restate the default. The uv cache stays where it is:
`build/runtime/tool-cache/uv` on GitHub and `/cache/uv` on GitLab.

### The repository follows the ETHOS code, not its superseded bootstrap requirement

The per-version path came from an older ETHOS requirement that bound each worktree's bootstrap to
`build/runtime/venv`. ETHOS moved Python execution to the root `.venv` on 6 August 2026, and its
artifact topology and entrypoint policy now treat `build/runtime/venv` as retired. Its accepted
repository-governance specification still states the earlier bootstrap; the ETHOS owner corrects
that requirement in its own Change, so this repository follows the code and the current topology.

## Risks / Trade-offs

- [A reused checkout could hold a `.venv` built for another Python version] → uv replaces a project
  environment whose interpreter does not satisfy the requested one, and each job requests its
  version explicitly.
- [The change is exercised only on the hosted runners] → Hosted acceptance follows publication;
  reverting the commit restores the previous projections.
