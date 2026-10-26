# Proposal

## Why

On 25 October 2026 every supply chain was asked to move to its latest stable release.
`.config/mise/config.toml` declares Node 26.12.0, Python 3.14.8, Ruff 0.17.1 and uv 0.13.4; the
current stable releases are Node 26.12.1, Python 3.14.9 (the newest 3.14 release), Ruff 0.17.2 and
uv 0.13.5. The GitHub workflow pins `actions/setup-python` v7.0.0 and `astral-sh/setup-uv` v10.3.0,
where v7.1.0 and v10.3.2 are current, and the GitLab jobs run the uv 0.13.4 images. `uv.lock`
resolves packages to releases older than their current stable ones, and OSV Scanner reports 11
known vulnerabilities in 6 of its packages, three of them Critical; stable releases fix eight.

## What Changes

- Declare Node 26.12.1, Python 3.14.9, Ruff 0.17.2 and uv 0.13.5 in `.config/mise/config.toml` and
  relock with `mise lock`.
- Pin `actions/setup-python` v7.1.0 and `astral-sh/setup-uv` v10.3.2 by commit, and the
  `ghcr.io/astral-sh/uv` 0.13.5 images for Python 3.12, 3.13 and 3.14 by index digest, in
  `.config/ci/pipeline.cue`, then regenerate `.github/workflows/verify.yml` and `.gitlab-ci.yml`.
- Refresh `uv.lock` with `uv lock --upgrade`. `requires-python` stays `>=3.12`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The pipelines keep their jobs, matrix and commands with new pins. `actions/checkout` v7.0.1,
`gitleaks/gitleaks-action` v3.0.0, Gitleaks 8.30.1, CUE 0.17.1, Taplo 0.10.0 and Prettier 3.9.10
are already current and stay. The Firecrawl images keep their reviewed digests, and Python 3.15 is
out of scope; the design explains both. Rebinding the repository to a newer ETHOS runtime is a hook
installation, not a file in this Change. `tasks.md` is the sole progress ledger.
