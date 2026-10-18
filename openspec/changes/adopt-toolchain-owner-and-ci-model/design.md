# Design

## Context

The repository's checks run `uv`, Prettier, taplo, Ruff and Gitleaks from the host's `PATH`;
nothing locks those tools. The GitHub workflow and the GitLab pipeline are written by hand and
already run the same owner scripts under `tools/ci/`, and contract tests bind their text. The
ETHOS runtime reports the missing toolchain owner, the missing pipeline model and two GitHub
steps that each run a shell sequence. The same runtime checks decision records against the
shared grammar, and the four records here use an older layout.

## Goals / Non-Goals

**Goals:** a locked toolchain owner with the three verbs, one model that generates both Forge
files, single-command CI steps, and a proof gate that refuses a drifted projection.

**Non-Goals:** changing ingestion behavior, the owner scripts, the CI images or runner selection,
or installing mise in hosted CI.

## Decisions

- mise owns the toolchain at the versions already in use: CUE 0.17.1, Gitleaks 8.30.1, Node
  26.12.0 with Prettier 3.9.10, Python 3.14.8, Ruff 0.17.1, taplo 0.10.0 and uv 0.13.1.
  `mise lock` records macOS ARM64, Linux ARM64 and Linux x64 checksums. The ETHOS behavior gate
  takes uv and Python from a declared toolchain, so the toolchain locks the host's current
  CPython; hosted CI keeps its uv images for Python 3.12 to 3.14.
- `tools/ci/project.py` runs the CUE on `PATH` after checking that it is the locked version, so
  the proof gate and `mise run check` render byte-identical projections; hosted CI does not run
  it.
- The model keeps every job, image, command and runner rule of the current pipelines. The GitHub
  uv environment stays on each uv step, so the setup actions keep their own cache settings.
- Prettier does not format mise's npm package locks, because mise writes them.
- The decision records keep each ruling, reason and revisit trigger. Their text moves into the
  five shared sections, alternatives that the old rationale rejected become explicit entries,
  and the fenced diagrams and the command example become prose.

## Risks / Trade-offs

- Generated YAML drops comments and decorative blank lines. Accepted: the comments move into the
  model, and the repository's conventions forbid decorative blank lines in machine-readable files.
- Restating a decision could shift its meaning. Mitigated: sentences keep their wording except
  the moved headings, the prose that replaces the diagrams and the command example, and
  DR-0003's note on the pipeline model.
- A host CUE of another version fails the projection gate. Accepted: `mise run check` selects the
  locked version.
