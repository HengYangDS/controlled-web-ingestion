# Controlled Web Ingestion Instructions

This repository is a portable, body-redacted implementation of Controlled Web
Ingestion. It is not a standing scraping service.

## Non-negotiable boundaries

- Preserve `requires-python >=3.12` without an upper bound; use the locked
  project environment rather than global Python packages.
- Do not persist body, HTML, Markdown, raw responses, credentials, private
  targets or account-state data in records, evidence, fixtures or Git history.
- `web-ingest` is the sole user-facing entry point. Do not expose raw
  Firecrawl as MCP, a default Agent tool, Hermes/Open WebUI integration or an
  automatic RAG writer.
- Firecrawl is on-demand, disposable and loopback-only. Do not add a daemon,
  reuse a pre-existing Redis/Postgres/listener, or change Docker daemon settings
  to make a validation pass.
- New targets require an explicit allowlist, purpose, budget, robots/MIME
  policy and evidence. Do not generalize from the reviewed public workloads.

## Verification

- Unit, contract and integration tests: `uv run --locked python tools/ci/run_tests.py`.
- Schema/declaration/evidence validation: `uv run --locked python tools/ci/validate_schemas.py`.
- Runtime validation is explicit: `tools/runtime/validate-authorized-workloads.sh`.

## Text layout

Follow [repository conventions](docs/reference/conventions.md): one blank line
separates adjacent semantic units; Python module-level definitions use two;
machine-readable files do not use decorative blank lines. Preserve final LF,
UTF-8, and no trailing whitespace.
