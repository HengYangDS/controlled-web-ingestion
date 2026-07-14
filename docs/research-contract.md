# Research Contract

## Primary object

Web Ingestion Benchmark is a controlled admission experiment for bounded
acquisition from approved public-web targets. It compares and constrains
candidate retrieval mechanisms without becoming a standing scraper or a general
content-delivery service.

## Authority boundary

The tracked policy, authorized workloads, code, tests, and body-redacted
evidence are authoritative. Runtime containers, temporary credentials, raw
responses, fetched bodies, and local caches remain outside Git and must not be
promoted as durable evidence.

## Inputs and outputs

Inputs are explicitly authorized public HTTP(S) URLs, a non-empty purpose,
selected mode, page budget, timeout, and staging root. Outputs are validated,
body-redacted staging receipts, promotion receipts, and sinkless bridge
manifests. Raw content is never the output interface.

## Admission and acceptance

Run the locked unit and contract suite for source changes. Full Firecrawl
runtime validation is an explicit, separately authorized operation requiring
reviewed local images and its documented disposable loopback boundary. A staged
receipt requires independent confirmation before promotion; `prepare-rag`
creates a manifest with `sink: null`.

## Non-goals

This project does not operate a standing crawler, expose Firecrawl as MCP or a
default agent tool, reuse private runtime services, persist raw content, or
write directly to RAG, Hermes, Open WebUI, or Project N.O.M.A.D.

## Portfolio interfaces

The sole Knowledge Systems transfer is a policy-validated, body-redacted staged
receipt for independent manual acceptance. The benchmark has no authority to
start Project N.O.M.A.D. services, change RAG policy, or alter any host runtime.
