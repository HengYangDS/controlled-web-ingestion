# Changelog

All notable changes to Controlled Web Ingestion are recorded here. This file follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The `web-ingest` command line, the repository's single entry point. `ingest` admits, collects and
  stages one request; `promote` explicitly promotes one staging receipt; `prepare-rag` prepares a
  body-redacted bridge manifest without delivering content to a sink; `validate-workloads` runs the
  reviewed workload set and writes one body-redacted evidence record.
- Policy-bound admission of explicitly authorized public web sources, acquisition through a
  replaceable adapter, and receipts that keep raw bodies, credentials and private targets out of
  tracked records.
- The repository checks, run locally with `mise run check` and in both Forges' pipelines: tests,
  schema and declaration evidence, documentation, source topology, the CI projection, formatting
  and secret scanning.
- `VERSION` as the only version source, and the MIT License.
