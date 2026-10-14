---
subject: controlled-web-ingestion:cli
role: reference
state: active
relations:
  canonical_for: user-facing command contract
---

# CLI Reference

`web-ingest` is the only user-facing runtime entry point.

```bash
web-ingest ingest --url URL --purpose TEXT --mode static|browser|crawl \
  --max-pages N --timeout-seconds N --stage-root ABSOLUTE_PATH
web-ingest promote --stage-root ABSOLUTE_PATH --receipt RECEIPT --confirm
web-ingest prepare-rag --bridge-root ABSOLUTE_PATH --receipt RECEIPT --confirm
web-ingest validate-workloads --evidence ABSOLUTE_PATH
```

Static mode uses the in-memory Trafilatura adapter. Browser and crawl modes preflight before any
container starts, then run one disposable, loopback-only Firecrawl topology under native Compose
and remove it after the request. `prepare-rag` writes a `sink: null` bridge manifest; it never
delivers content to a RAG sink. `validate-workloads` runs the reviewed workload set described in
[Runtime Validation](runtime-validation.md).
