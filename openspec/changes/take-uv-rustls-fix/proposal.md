# Proposal

## Why

The repository declares uv 0.13.6 in `.config/mise/config.toml`, the GitHub workflow installs it
through setup-uv, and the GitLab jobs run its images. uv 0.13.6 embeds rustls 0.23.45, and four
RustSec advisories, GHSA-c8m5-c952-6cm4 among them, are fixed in rustls 0.23.46. uv 0.13.7,
published on 3 November 2026 at 02:45 UTC, pins rustls 0.23.46. The owner's direction of
2 November 2026 is that every supply chain moves to its latest stable release.

## What Changes

- Declare uv 0.13.7 in `.config/mise/config.toml` and lock it again with `mise lock`.
- Set `_uv` to 0.13.7 in `.config/ci/pipeline.cue`, pin the `ghcr.io/astral-sh/uv` 0.13.7 images
  for Python 3.12, 3.13 and 3.14 by index digest, and regenerate `.github/workflows/verify.yml` and
  `.gitlab-ci.yml`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

`.config/mise/config.toml`, `.config/mise/mise.lock`, `.config/ci/pipeline.cue` and its two
projections. The pipelines keep their jobs, matrix and commands, setup-uv stays v10.3.3, and
`uv.lock` and the Firecrawl images stay; the design explains why. `tasks.md` is the sole progress
ledger.
