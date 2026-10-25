# Design

## Context

`.config/mise/config.toml` owns the toolchain and `.config/mise/mise.lock` its checksums.
`.config/ci/pipeline.cue` owns both pipelines, and `tools/ci/project.py` renders
`.github/workflows/verify.yml` and `.gitlab-ci.yml` from it; its `--check` mode is a proof gate.
The GitLab jobs run in `ghcr.io/astral-sh/uv` images pinned by index digest, one per supported
Python, and their tag follows the uv release that mise declares. On 25 October 2026 the newest
releases were read from mise, PyPI, the GitHub releases API and the image registry.

## Goals / Non-Goals

**Goals:**

- Move the mise tools, the pinned actions, the uv images and the Python lock to their current
  stable releases, keeping the Python 3.12 support line.

**Non-Goals:**

- Changing jobs, commands, the Python matrix or runner selection.
- Adopting Python 3.15 for the mise runtime or the CI matrix.
- Moving the Firecrawl images.

## Decisions

### The runtime stays on Python 3.14

Python 3.15.1 is the newest stable release, but `fastuuid` 0.14.0 and `pyyaml` 6.0.3 still publish
no CPython 3.15 wheel, so a 3.15 environment would build them from source. The mise Python moves to
3.14.9, the newest 3.14 release, and the matrix stays 3.12–3.14.

### The Firecrawl images keep their reviewed digests

`system/supply-chain/firecrawl-provenance.json` binds each of the five images in the isolated
Firecrawl stack to a reviewed manifest digest, a local image identity and a verification method,
and Compose runs only those objects. On 25 October 2026 two of them had newer tags: the
`ghcr.io/firecrawl/firecrawl` API at 2.11.209 against the reviewed 2.10.19, and `rabbitmq` at
4.4.0-alpine against 4.3.6-alpine. `redis` 8.10.2-alpine is current, and `playwright-service` and
`nuq-postgres` publish only a moving `latest` tag. Moving an image needs a new provenance review
with image acquisition and the product's workload validation, which runs the disposable stack
against the reviewed public workloads. That is more than a lock refresh, so it returns as its own
Change.

### Action inputs carry over unchanged

setup-python v7.1.0 adds the optional `mirror` and `mirror-token` inputs and changes nothing the job
uses. setup-uv v10.3.1 fixes a cache-save warning, and v10.3.2 adds the known checksums for uv
0.13.5, the release the job now installs. The job keeps its `python-version`, `version` and
`enable-cache` inputs.

### Advisories that only a prerelease fixes stay until a stable fix ships

OSV Scanner reads the refreshed lock before anything is installed from it. The refresh removes
every advisory that a stable release fixes. Twisted 26.4.0 keeps advisories that only the
prerelease 26.10.0rc1 fixes, or that nothing fixes yet, and PYSEC-2017-83 names no fixed scrapy
release. Prereleases are outside this refresh, so those advisories remain until a stable release
fixes them.

## Risks / Trade-offs

- [The lock refresh can move a dependency across a major version] → OSV Scanner reads the
  refreshed lock before installation, and the repository's tests and checks run on the refreshed
  environment before proof.
- [The new actions and images are exercised only on the hosted runners] → Hosted acceptance follows
  publication, which is outside this local pass.
