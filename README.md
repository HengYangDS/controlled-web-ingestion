# Web-Ingestion Framework Benchmark

This is an isolated, body-redacted admission benchmark. It compares Firecrawl, Crawl4AI, Crawlee, Scrapy plus Trafilatura, and the Jina Reader baseline under the same public workload.

## Boundaries

- Python dependencies are scoped to `.venv`; no global package is installed.
- Firecrawl runs only under the `web-ingestion-firecrawl-bench` Compose project on `127.0.0.1:13002`.
- If local Firecrawl runtime credentials are configured, store them outside this tree in `~/.config/agentic/credentials/firecrawl.env` with owner-only permissions and pass that file explicitly through Compose `--env-file`. Plaintext credentials do not belong in this benchmark directory.
- Existing Hermes, Open WebUI, `nomad_redis`, Postgres, MCP, RAG, and personal/private targets are excluded.
- Durable results contain only normalized metadata, hashes, resource samples, and redacted errors.
- `policy.json` is the enforceable admission baseline: public HTTP(S) only, redirect-hop validation, robots/crawl-delay, one request per origin, timeout/cancellation, allowed media types, and body-redacted provenance.
- `admission.py` creates a staging ledger only. Promotion is an explicit local act; it does not write RAG, create MCP tools, alter Open WebUI, or add Hermes capabilities.

## Record contract

Each result contains candidate/case identifiers, request/final/source URLs, timestamps, status, a content digest, title, discovery count, resource sample, artifact paths, and a redacted error. Raw fetched bodies are rejected by `validate_record`.

## Controlled Web-Ingestion (M2–M5)

`web_ingest.py` is the only user-facing ingestion command in this experiment.
Every `ingest` request must provide a URL, non-empty purpose, explicit mode,
page budget, timeout, and staging root. It performs public-target and
redirect-hop admission, robots evaluation, allowed-MIME checking, bounded
extraction, content-digest deduplication, and body-redacted staging. The
only routes are `static` -> Trafilatura and `browser` / `crawl` -> the
disposable Firecrawl runner. The latter is not a general API entry point.

The data-plane transitions are separate and explicit:

```bash
cd <repository-root>

# Stage approved content. Browser/crawl starts no service until preflight passes.
uv run --locked python web_ingest.py ingest \
  --url https://example.com/ \
  --purpose 'approved, bounded ingestion' \
  --mode static --max-pages 1 --timeout-seconds 45 \
  --stage-root /absolute/controlled-stage

# A staged receipt needs independent confirmation before promotion.
uv run --locked python web_ingest.py promote \
  --stage-root /absolute/controlled-stage \
  --receipt /absolute/controlled-stage/staging/RECEIPT.json --confirm

# This writes only a body-redacted manifest; no RAG sink is configured.
uv run --locked python web_ingest.py prepare-rag \
  --bridge-root /absolute/controlled-bridge \
  --receipt /absolute/controlled-stage/promoted/RECEIPT.json --confirm
```

Receipts and bridge manifests never persist body, HTML, Markdown, or raw
responses. A duplicate receipt cannot be promoted. `prepare-rag` creates a
manifest with `sink: null`; it is not an ingestion-to-RAG delivery command.
The controlled M2–M5 validation is:

```bash
scripts/web-ingestion-m2-m5-validate.sh
```

It reads only `ops/web-ingestion-authorized-workloads.json`, runs static,
duplicate, promotion, bridge preparation, browser, and ten-page crawl cases,
then exercises a deliberately failing private-loopback request and verifies
cleanup. Its durable, body-redacted output is
`evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-validation.json`.
The operational runbook is
`docs/benchmarks/2026-07-14-web-ingestion-m2-m5-runbook.md`.
The complete closeout, bounded-housekeeping receipt, and lessons learned are
in `docs/benchmarks/2026-07-14-web-ingestion-m2-m5-closeout-retrospective.md`.

## Firecrawl M1 isolated run

`scripts/firecrawl-isolated-benchmark.sh` is the only Firecrawl service runner in this experiment. It starts temporary Brew-managed Redis and RabbitMQ on benchmark-only loopback ports, combines them with pinned official GHCR Firecrawl images, publishes only `127.0.0.1:13002`, records body-redacted evidence, and tears everything down even on failure. It refuses an existing Compose project or occupied benchmark ports rather than taking ownership of another process.

The runner requires that `redis` and `rabbitmq` have already been admitted and installed through Homebrew. It does not change Docker daemon configuration or use Docker Hub/mirror images. Its `nuq-postgres` dependency is the official Firecrawl image pinned as part of the Firecrawl suite; it is network-internal, uses a disposable tmpfs data directory, and is removed with the Compose project.

The 2026-07-14 M1 run completed static, JavaScript, and bounded ten-page crawl cases, rejected a service-side loopback scrape request, and left no benchmark container, volume, network, listener, or virtual environment. M2–M5 then added the policy-controlled CLI, provenance gate, authorized public-workload validation, explicit promotion, and sinkless bridge. The decision remains **admit-as-service only within this runner's on-demand, disposable, loopback-only boundary**. It is not authorization for a standing daemon, MCP/default-tool registration, Hermes/Open WebUI integration, or direct RAG writes. See `docs/benchmarks/2026-07-14-web-ingestion-firecrawl-m1-closeout.md` and `docs/benchmarks/2026-07-14-web-ingestion-m2-m5-runbook.md`.

### GHCR transport recovery

When this host's Docker client truncates long GHCR blob streams, first import the fixed official images through the range-verified recovery path:

```bash
python3 scripts/import-pinned-firecrawl-images.py --workers 1
```

`ops/firecrawl-images.json` contains only reviewed official GHCR repository/tag/platform-manifest digests. The importer fetches exact byte ranges from short-lived official signed GHCR URLs, verifies every blob against the manifest SHA-256 digest, builds a local `docker load` archive, then runs `docker load`. It does not set a registry mirror, change Docker configuration, or accept a replacement source. A failed transfer keeps only digest-addressed verified partial chunks in its explicit cache directory for resumption; no partial or mismatched blob is loaded.
