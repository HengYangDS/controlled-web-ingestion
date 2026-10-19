# Design

## Context

`.config/mise/config.toml` owns the toolchain and `.config/ci/pipeline.cue` owns both pipelines;
`tools/ci/project.py` renders `.github/workflows/verify.yml` and `.gitlab-ci.yml` from the model,
and its `--check` mode is a proof gate. The GitHub job installs Python with
`actions/setup-python`, uv with `astral-sh/setup-uv` and scans with `gitleaks/gitleaks-action`;
the GitLab jobs run in digest-pinned `ghcr.io/astral-sh/uv` and `ghcr.io/gitleaks/gitleaks`
images. On 19 October 2026 the mise tools, the npm Prettier lock and both images were already at
their current stable releases.

## Goals / Non-Goals

**Goals:**

- Move every pinned action, the GitHub Gitleaks request and the Python lock to their current stable
  releases, keeping the Python 3.12 support line.
- Make the contract tests follow the toolchain owner, so a later upgrade changes one declaration.

**Non-Goals:**

- Changing jobs, commands, the Python matrix or runner selection.
- Adopting Python 3.15 for the mise runtime or the CI matrix.

## Decisions

### The runtime stays on Python 3.14

Python 3.15.0 is the newest stable release, but the refreshed lock has no CPython 3.15 wheel for
`brotli` 1.2.0, `fastuuid` 0.14.0 and `pyyaml` 6.0.3, so a 3.15 environment would build them from
source. The mise Python stays at 3.14.8, the newest 3.14 release, and the matrix stays 3.12–3.14.

### Action inputs carry over unchanged

The job uses only `python-version`, `enable-cache` and `fetch-depth`, and each new release keeps
them. Since v5, setup-uv's breaking releases broadened the default cache key glob, made environment
activation opt-in, removed inputs the job does not use, moved to Node 24, stopped publishing
floating tags, stopped pruning the cache by default and disabled the `auto` cache for sensitive
events. The job sets `enable-cache: true`, runs on no sensitive event and never passed a Python
version to setup-uv, so it relied on none of these defaults. checkout v7 refuses fork pull request
checkouts only for `pull_request_target` and `workflow_run`, and setup-python v7 removed only the
`pip-install` input; the workflow uses neither.

### The contract tests read the toolchain owner

The tests asserted each action commit and the Gitleaks version as literals, so every upgrade edited
them and the GitHub Gitleaks request drifted from mise unnoticed. They now require every action to
be pinned by a 40-character commit and the Gitleaks and uv versions in both projections to equal
the mise declaration.

## Risks / Trade-offs

- [The lock refresh moves several dependencies across a major version] → The repository's tests
  and checks run on the refreshed environment before proof, and hosted CI runs them on Python
  3.12, 3.13 and 3.14 after publication.
- [The new action releases are only exercised on GitHub] → Publication runs the workflow on the
  published head; its result is recorded as hosted acceptance.
