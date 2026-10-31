# Proposal

## Why

The owner's standing direction is that every supply chain moves to its latest stable release. On
31 October 2026, `.config/mise/config.toml` declares Node 26.12.1, Python 3.14.9, Ruff 0.17.2 and
uv 0.13.5 with a Mise floor of 2026.10.10, while Node 26.13.0, Python 3.14.10 (the newest 3.14
release), Ruff 0.17.3, uv 0.13.6 and Mise 2026.10.24 are current. The GitHub workflow pins
`astral-sh/setup-uv` v10.3.2 where v10.3.3 is current, and the GitLab jobs run the uv 0.13.5
images. `uv.lock` resolves packages to older releases. OSV reports eight Twisted advisories, seven
of which the stable Twisted 26.10.0 now fixes, and one scrapy advisory with no fixed release. The
isolated Firecrawl stack runs `redis:8.10.2-alpine`, while `8.10.3-alpine` is the newest 8.x Alpine
image.

## What Changes

- Declare Node 26.13.0, Python 3.14.10, Ruff 0.17.3 and uv 0.13.6, and a Mise floor of 2026.10.24,
  in `.config/mise/config.toml`, and lock it again with `mise lock`.
- Pin `astral-sh/setup-uv` v10.3.3 by commit and the `ghcr.io/astral-sh/uv` 0.13.6 images for
  Python 3.12, 3.13 and 3.14 by index digest in `.config/ci/pipeline.cue`, and regenerate
  `.github/workflows/verify.yml` and `.gitlab-ci.yml`.
- Refresh `uv.lock` with `uv lock --upgrade`. `requires-python` stays `>=3.12`.
- Move Redis to `docker.io/library/redis:8.10.3-alpine`, pinned by its index digest, in
  `system/supply-chain/firecrawl-provenance.json` and
  `system/projections/firecrawl-isolated-compose.yaml`, and commit the runtime validation record of
  the moved set under `evidence/verification/`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Ingestion behavior and its contracts are unchanged, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The pipelines keep their jobs, matrix and commands with new pins. CUE 0.17.1, Taplo 0.10.0,
Prettier 3.9.10, Gitleaks 8.30.1, `actions/checkout` v7.0.1, `actions/setup-python` v7.1.0 and
`gitleaks/gitleaks-action` v3.0.0 are already current and stay. The Firecrawl API stays on the
v2.11.0 release image, RabbitMQ 4.4.0 is current, and the Playwright service and NuQ Postgres keep
their reviewed digests; the design explains these and Python 3.15. Rebinding the repository to a
newer ETHOS runtime is a hook installation, not a file in this Change. `tasks.md` is the sole
progress ledger.
