# Web-Ingestion Benchmark Instructions

This repository is a portable, body-redacted publication of a controlled
web-ingestion admission experiment. It is not a standing scraping service.

## Non-negotiable boundaries

- Preserve `requires-python >=3.12` without an upper bound; use the locked
  project environment rather than global Python packages.
- Do not persist body, HTML, Markdown, raw responses, credentials, or private
  target data in records, evidence, fixtures, or Git history.
- `web_ingest.py` is the only user-facing entry point. Do not expose the raw
  Firecrawl API as MCP, a default Agent tool, Hermes/Open WebUI integration, or
  an automatic RAG writer.
- Firecrawl is on-demand, disposable, and loopback-only. Do not add a daemon,
  reuse a pre-existing Redis/Postgres/listener, or change Docker daemon
  settings to make a benchmark pass.
- New targets require explicit allowlist, purpose, budget, robots/MIME policy,
  and evidence. Do not generalize from the three current public workloads.

## Verification

- Unit and contract tests: `uv run --locked python -m unittest discover -s tests -v`.
- Shell syntax: `bash -n scripts/firecrawl-isolated-benchmark.sh` and
  `bash -n scripts/web-ingestion-m2-m5-validate.sh`.
- Full runtime validation requires reviewed local images, Homebrew Redis and
  RabbitMQ, and explicit authorization; it is intentionally not a generic CI
  task.
