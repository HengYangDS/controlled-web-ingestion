# Design

## Context

`.config/mise/config.toml` owns the toolchain and `.config/mise/mise.lock` its checksums.
`.config/ci/pipeline.cue` owns both pipelines, and `tools/ci/project.py` renders
`.github/workflows/verify.yml` and `.gitlab-ci.yml` from it; its `--check` mode is a proof gate.
The GitLab jobs run in `ghcr.io/astral-sh/uv` images pinned by index digest, one per supported
Python, and their tag follows the uv release that Mise declares.
`system/supply-chain/firecrawl-provenance.json` binds each image of the isolated Firecrawl stack to
a reviewed digest, a local image identity and a verification method, and
`system/projections/firecrawl-isolated-compose.yaml` runs only those objects. On 31 October 2026
the newest releases were read from Mise, PyPI, the GitHub releases API, Docker Hub and GHCR.

## Goals / Non-Goals

**Goals:**

- Move the Mise tools and floor, the pinned action, the uv images, the Python lock and the Redis
  image to their current stable releases, keeping the Python 3.12 support line.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection or the workload set.
- Adopting Python 3.15 for the Mise runtime or the CI matrix.
- Moving the Firecrawl API, RabbitMQ, the Playwright service or NuQ Postgres.

## Decisions

### The runtime stays on the Python 3.14 line

Python 3.15.2 is the newest stable release, but `fastuuid` 0.14.0 and `pyyaml` 6.0.3, both the
newest releases, still publish no CPython 3.15 wheel, so a 3.15 environment would build them from
source, `fastuuid` with a Rust toolchain. The Mise Python moves to 3.14.10, the newest 3.14 release,
and the matrix stays 3.12 to 3.14.

### Action inputs carry over unchanged

setup-uv v10.3.3 is a patch release of the pinned v10.3 line. The job keeps its `python-version`,
`version` and `enable-cache` inputs.

### The lock takes the stable Twisted fix

`uv lock --upgrade` moves Twisted to 26.10.0, the first stable release that fixes seven of the eight
advisories; the eighth, GHSA-8pqf-f4m5-798g, and scrapy's PYSEC-2017-83 have no fixed release and
remain until one exists. OSV reads the refreshed lock before anything is installed from it.

### Only Redis moves in the Firecrawl stack

v2.11.0 is still the newest stable Firecrawl release, so the API stays on its release image
2.10.30. RabbitMQ 4.4.0 is still the newest 4.x Alpine image. The Playwright service and NuQ
Postgres publish only moving `latest` and post-release `sha-` tags, so they keep their reviewed
digests, as `refresh-firecrawl-images` decided. Redis 8.10.3 is a patch release of the pinned 8.10
line; it is pinned by index digest, acquired with `docker compose pull --policy always`, and the
moved set must pass `web-ingest validate-workloads` before its record is committed.

## Risks / Trade-offs

- [The lock refresh can move a dependency across a major version] → OSV reads the refreshed lock
  before installation, and every `mise run check` command runs on the refreshed environment before
  proof.
- [The new action and images are exercised only on the hosted runners] → Hosted acceptance follows
  publication of the landed head.
- [Redis 8.10.3 changes behavior the stack relies on] → The runtime acceptance drives the static,
  browser and crawl workloads through the moved set; a failure keeps 8.10.2.
