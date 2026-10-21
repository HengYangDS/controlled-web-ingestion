# Change: Patch uv For The Compromised emSign Root

## Why

GitHub advisory GHSA-hq85-5cpj-mr62, published on 20 October 2026 and rated critical, reports that
uv before 0.13.4 trusts the `emSign ECC Root CA - G3` root in its vendored `webpki-root-certs`
bundle. Eight eMudhra intermediate certificates that chain to that root have compromised private
keys, so a holder of one can issue certificates that uv accepts for any host name and intercept its
TLS connections. uv 0.13.4 removes the root.

This repository declares uv 0.13.1 in `.config/mise/config.toml`, in its lock and in the three
GitLab job images, so local runs and GitLab CI resolve and download packages through the affected
trust store. The GitHub job requests no uv release: setup-uv finds none in `uv.toml` or
`pyproject.toml` and installs the newest one, which was 0.13.3 in run 39403774544 on
20 October 2026. Its uv therefore follows the release feed instead of the declared toolchain,
although the design of `converge-stable-supply` intended both projections to follow the mise
declaration.

## What Changes

- Declare uv 0.13.4 in `.config/mise/config.toml` and relock it with `mise lock`.
- Name the uv release once in `.config/ci/pipeline.cue` and move the three GitLab job images to the
  uv 0.13.4 Debian Trixie images, each pinned by the digest of its image index.
- Pass the declared release to setup-uv in the GitHub job, and require in the CI contract test that
  the GitHub projection requests the mise uv version.
- Regenerate `.github/workflows/verify.yml` and `.gitlab-ci.yml` from the model.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

Both pipelines keep their jobs, matrix and commands; only the uv release and the image digests
change. `uv.lock`, the actions and the other tools stay as they are. Hosted acceptance of both
pipelines follows the landing. `tasks.md` is the sole progress ledger.
