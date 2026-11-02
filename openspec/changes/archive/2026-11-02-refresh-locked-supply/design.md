# Design

## Context

`uv.lock` resolves the ranges in `pyproject.toml`.
`system/supply-chain/firecrawl-provenance.json` binds each image of the isolated Firecrawl stack to
a reviewed digest, a local image identity and a verification method, and
`system/projections/firecrawl-isolated-compose.yaml` runs only those objects. On 2 November 2026
the newest releases were read from Mise, PyPI, the GitHub releases API, Docker Hub and GHCR.

## Goals / Non-Goals

**Goals:**

- Move the Python lock and the RabbitMQ image to their current stable releases, keeping the Python
  3.12 support line.
- Give a public target the same TLS answer on every host, so the documented runtime acceptance runs
  as written.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection or the workload set.
- Adopting Python 3.15 for the Mise runtime or the CI matrix.
- Moving the Firecrawl API, Redis, the Playwright service or NuQ Postgres.
- Changing `/etc/ssl/cert.pem` or any other host trust.

## Decisions

### The runtime stays on the Python 3.14 line

Python 3.15.2 is the newest stable release, but `fastuuid` 0.14.0 and `pyyaml` 6.0.3, both the
newest releases, still publish no CPython 3.15 wheel, so a 3.15 environment would build them from
source, `fastuuid` with a Rust toolchain. Mise's Python 3.14.10 is the newest 3.14 release.

### The lock takes python-dateutil 4.0

`uv lock --upgrade` moves `python-dateutil` from 3.0.0 to 4.0.0, the one major move, which
`dateparser` and `htmldate` allow. Its notes list one stricter behavior, in `isoparse`, and no
installed package outside `dateutil` calls it. It no longer needs `six`, so the lock drops `six`.

### Upstream ranges hold some lock rows

`pyee` 14.0.0, `snowballstemmer` 2.2.0 and `xxhash` 3.8.2 have newer major releases on PyPI, and
`uv lock --upgrade` keeps them because `playwright`, `patchright` and `crawl4ai` refuse those
releases. An override would claim a compatibility that the dependents do not declare, so the lock
keeps what the resolver selects.

### The static transport trusts the locked roots

`default_transport` let `http.client` build its TLS context, which loads the host's bundle. For this
Python on macOS that is `/etc/ssl/cert.pem`. At 22:07 on 2 November 2026 that file lost
`AAA Certificate Services` and `emSign ECC Root CA - G3`, through Homebrew's `emudhra_certificates.rb`,
which applies the mitigation in Apple's advisory. The chain of `https://example.com/` ends in
`SSL.com TLS ECC Root CA 2022`, cross-signed by `AAA Certificate Services`, and the file holds no
root of that name, so `validate-workloads` failed at its first fetch, before it started any topology.

Restoring the root would undo a security mitigation, and setting `SSL_CERT_FILE` for one run would
leave the documented command failing. The transport now builds its context from `certifi`. `uv.lock`
already pins `certifi` for `requests`, `httpx` and `trafilatura`, so no package is added. It holds
`SSL.com TLS ECC Root CA 2022` and neither mitigated root, and a lock refresh moves it with the rest
of the supply. `truststore` is also in the lock and would follow Apple's block on macOS, but its
answer would change with the host, and the evidence record has to mean the same thing on any host.

The contract test runs a real TLS server whose self-signed certificate the host's trust accepts,
which its control request shows, and requires `default_transport` to refuse it. That adds
`cryptography`, already locked for `scrapy`, to the `dev` group as a direct test dependency.

### RabbitMQ takes the republished index

RabbitMQ 4.4.0 is still the newest 4.x Alpine release, and its tag now resolves to a republished
index, as Redis's did on 26 October. The engine resolves the new index to the local image ID the old
one gave on linux/arm64, so only the record's digest moves. The moved set passes
`web-ingest validate-workloads` before its record is committed.

### The Firecrawl API and its companions stay

v2.11.0 is still the newest stable Firecrawl release, so the API stays on its release image 2.10.30,
whose linux/arm64 manifest is unchanged. The Playwright service and NuQ Postgres publish only moving
`latest` and post-release `sha-` tags, and each of those builds comes after v2.11.0, so the reasoning
of `refresh-firecrawl-images` holds. Their `latest` builds carry dependency security fixes from
October 2026 that no release contains; a later Firecrawl release moves them with the API.

## Risks / Trade-offs

- [The lock refresh can move a dependency across a major version] → OSV reads the refreshed lock
  before installation, and every `mise run check` command and the runtime acceptance run on the
  refreshed environment before proof.
- [The republished RabbitMQ image changes behavior the stack relies on] → The runtime acceptance
  drives the static, browser and crawl workloads through the moved set; a failure keeps the old
  digest.
- [A public target's chain reaches only a root that `certifi` does not hold] → The transport refuses
  it, and the fetch fails closed. A lock refresh moves the roots; nothing widens trust for one target.
- [Python's default trust still reaches other code] → `tools/benchmark/run_framework_comparison.py`
  fetches `r.jina.ai` with the default context, and that host verifies today. It is a measured
  baseline outside the runtime package, so this Change leaves it.
