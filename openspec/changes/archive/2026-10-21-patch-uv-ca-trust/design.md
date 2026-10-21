# Design

## Context

`.config/mise/config.toml` owns the toolchain, and `.config/mise/mise.lock` records each tool's
release assets with their checksums and provenance. `.config/ci/pipeline.cue` owns both pipelines;
`tools/ci/project.py` renders `.github/workflows/verify.yml` and `.gitlab-ci.yml` from it, and its
`--check` mode is a proof gate. The GitLab jobs run in digest-pinned `ghcr.io/astral-sh/uv` images.
The GitHub job installs uv with setup-uv v10.3.0 and passes it only `enable-cache`. The contract
tests require the GitLab images to carry the mise uv version and every action to be pinned by
commit, but say nothing about the uv release on GitHub.

## Goals / Non-Goals

**Goals:**

- Run uv 0.13.4 wherever this repository runs uv: locally through mise, in every GitLab job and in
  every GitHub job.
- Keep one declared uv release that the contract tests compare both projections against.

**Non-Goals:**

- Upgrading the actions, the other tools, the Python matrix or `uv.lock`.
- Changing jobs, commands or runner selection.

## Decisions

### uv 0.13.4 is the release

uv 0.13.4 is the first release without the emSign root and, on 21 October 2026, the newest stable
uv release. Its Debian Trixie images for Python 3.12, 3.13 and 3.14 exist. Each image is pinned by
the digest of its OCI image index, read from the registry's `Docker-Content-Digest` header and
checked against the digest of the returned index.

### GitHub requests the declared release

Without a `version` input, setup-uv reads a `required-version` from `uv.toml` or `pyproject.toml`
and otherwise installs the newest release. A `required-version` in `pyproject.toml` would also stop
an older uv from running locally, but it would declare the release a second time beside mise. The
job instead passes the release as setup-uv's `version` input from the CI model, and the contract
test requires it to equal the mise declaration, as it already requires for Gitleaks.

### The model names the release once

`pipeline.cue` interpolates one `_uv` value into the three image tags and the setup-uv input, so a
later upgrade changes the release in one place there, beside the digests that must change with it.

## Risks / Trade-offs

- [The GitHub job no longer picks up new uv releases by itself] → Each later uv upgrade is one
  declared change, as it already is for GitLab and local runs; this advisory shows why the
  declaration, not the release feed, should decide.
- [The images and setup-uv only run on the Forges] → Publication runs the GitHub workflow on the
  published head, and the GitLab pipeline runs once the intranet Forge is reachable. Their results
  are recorded as hosted acceptance.
