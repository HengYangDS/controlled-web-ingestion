# Design

## Context

The repository's checks run `uv`, Prettier, taplo, Ruff and Gitleaks from the host's `PATH`;
nothing locks those tools. The GitHub workflow and the GitLab pipeline are written by hand and
already run the same owner scripts under `tools/ci/`, and contract tests bind their text. The
ETHOS runtime reports the missing toolchain owner, the missing pipeline model and two GitHub
steps that each run a shell sequence.

## Goals / Non-Goals

**Goals:** a locked toolchain owner with the three verbs, one model that generates both Forge
files, single-command CI steps, and a proof gate that refuses a drifted projection.

**Non-Goals:** changing ingestion behavior, the owner scripts, the CI images or runner selection,
or installing mise in hosted CI.

## Decisions

- mise owns the toolchain at the versions already in use: CUE 0.17.1, Gitleaks 8.30.1, Node
  26.12.0 with Prettier 3.9.10, Ruff 0.17.1, taplo 0.10.0 and uv 0.13.1. `mise lock` records
  macOS ARM64, Linux ARM64 and Linux x64 checksums.
- `tools/ci/project.py` runs the CUE on `PATH` after checking that it is the locked version, so
  the proof gate and `mise run check` render byte-identical projections; hosted CI does not run
  it.
- The model keeps every job, image, command and runner rule of the current pipelines. The GitHub
  uv environment stays on each uv step, so the setup actions keep their own cache settings.
- Prettier does not format mise's npm package locks, because mise writes them.

## Risks / Trade-offs

- Generated YAML drops comments and decorative blank lines. Accepted: the comments move into the
  model, and the repository's conventions forbid decorative blank lines in machine-readable files.
- A host CUE of another version fails the projection gate. Accepted: `mise run check` selects the
  locked version.
