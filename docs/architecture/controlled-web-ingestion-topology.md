---
subject: web-ingestion:topology
role: design
state: active
relations:
  canonical_for: controlled-web-ingestion repository topology and ETHOS adoption boundary
  supersedes: flat benchmark-root organization
  implemented_by: docs/plans/2026-07-14-controlled-web-ingestion-topology-implementation.md
---

# Controlled Web Ingestion: Repository Topology and ETHOS Adoption Design

## Status

Active. This approved design is the implementation boundary for the repository reorganization
and for subsequent ETHOS adoption. It does not authorize a standing service,
unbounded crawling, direct RAG delivery, MCP/default-tool registration, Hermes
or Open WebUI integration.

## 1. Root Position

The repository is **Controlled Web Ingestion**: a policy-bound, evidence-driven
ingress capability for explicitly authorized web sources.

It receives a declared ingestion intent, proves that the target and requested
route are admissible, performs bounded acquisition through a replaceable
adapter, and emits a body-redacted receipt. Promotion is explicit; the RAG
bridge is an auditable interface whose default sink is `null`.

```text
Intent -> Policy -> Route -> Acquisition -> Receipt -> Promotion -> Bridge -> Evidence
```

Benchmarking is therefore a quality and evidence lane. It is not the product
identity. Firecrawl, Crawl4AI, Crawlee, Scrapy plus Trafilatura, and Jina Reader
are candidate adapters or measured baselines, not repository owners.

## 2. Invariants

1. Every ingestion request declares URL, purpose, mode, page budget, timeout,
   and stage root.
2. Public-target validation, every redirect hop, robots, MIME, route budget,
   and final adapter-reported source URL are independently admitted.
3. Body, HTML, Markdown, raw responses, credentials, private targets, and
   account-state data never enter tracked receipts or evidence.
4. Duplicate content may be staged for audit but may not be promoted.
5. Promotion and bridge preparation require explicit confirmation. The default
   bridge has no sink and performs no RAG delivery.
6. Firecrawl is only an on-demand, disposable, loopback-only adapter. It never
   becomes a standing daemon or a shared dependency of another local service.
7. Framework changes, policy changes, image/provenance changes, Compose changes,
   new targets, or a new integration surface require fresh evidence.

## 3. Terminal Topology

```text
.
├── src/web_ingestion/
│   ├── __init__.py
│   ├── cli.py
│   ├── contracts.py
│   ├── controller.py
│   ├── policy.py
│   ├── transport.py
│   ├── staging.py
│   ├── bridge.py
│   ├── adapters/
│   │   ├── static.py
│   │   └── firecrawl.py
│   └── supply_chain/
│       ├── provenance.py
│       ├── ghcr_archive.py
│       ├── ghcr_ranges.py
│       └── ghcr_registry.py
├── system/
│   ├── policies/
│   ├── projections/
│   ├── supply-chain/
│   └── schemas/
├── tools/
│   ├── ci/
│   ├── runtime/
│   └── supply-chain/
├── tests/
│   ├── unit/
│   ├── contract/
│   └── integration/
├── docs/
│   ├── start/
│   ├── architecture/
│   ├── decisions/
│   ├── evidence/
│   ├── reference/
│   ├── plans/
│   └── history/
├── evidence/
│   ├── benchmarks/
│   └── verification/
├── openspec/
└── .ethos/
```

The topology adopts ETHOS's semantic discipline, not its product size. This is
a single Python package and one controlled CLI; it does not require an ETHOS
monorepo, product packages, a separate runtime database, or a copy of ETHOS
internals.

## 4. Code Contracts

### 4.1 `src/web_ingestion/`

| Unit | Owns | Does not own |
| --- | --- | --- |
| `contracts.py` | request, receipt, outcome, error types | transport, policy side effects |
| `policy.py` | target, redirect, robots, MIME and budget decisions | HTTP connection or persistence |
| `transport.py` | bounded public HTTP fetches | extraction, promotion or routing |
| `controller.py` | request lifecycle and route selection | adapter-specific protocol details |
| `staging.py` | receipt validation, digest dedupe, explicit promotion | content extraction |
| `bridge.py` | promoted-receipt validation and sinkless manifest | default delivery sink |
| `adapters/static.py` | in-memory static extraction | persistent service lifecycle |
| `adapters/firecrawl.py` | loopback Firecrawl request protocol | host policy admission or daemon lifecycle |
| `supply_chain/*` | reviewed GHCR identity and range-verified import | ingestion policy or adapter routing |
| `cli.py` | explicit user commands and argument contract | raw Firecrawl public API exposure |

The stable executable is a `web-ingest` console command defined in
`pyproject.toml`. No root-level implementation module remains after migration.

### 4.2 `system/`

`system/` holds declarative, reviewed repository truth:

| Root | Contents |
| --- | --- |
| `system/policies/` | ingestion policy and authorized workload declarations |
| `system/projections/` | route map and disposable Compose projection |
| `system/supply-chain/` | reviewed images and Firecrawl provenance records |
| `system/schemas/` | stage receipt, promotion receipt, bridge manifest, and evidence schemas |

No secrets, runtime state, bodies, or generated result files belong here.

### 4.3 `tools/`

`tools/ci/` is the owner of every CI command. `.gitlab-ci.yml` calls these
scripts rather than duplicating Python, shell, security, or documentation
commands inline. `tools/runtime/` owns disposable Firecrawl invocation and
authorized workload validation. `tools/supply-chain/` owns provenance and image
import utilities.

## 5. Documentation and Evidence Kernel

The documentation root follows the ETHOS common kernel:

| Root | Role |
| --- | --- |
| `docs/decisions/` | durable rulings, scope, and revisit triggers |
| `docs/evidence/` | indexes for dated proof and closeout records |
| `docs/reference/` | stable contracts, route semantics, CLI and operations reference |
| `docs/history/` | superseded benchmark reports and migration history |
| `docs/architecture/` | topology, data-flow and adapter boundaries |
| `docs/start/` | first-run and contribution path |
| `docs/plans/` | approved implementation plans only |

Each canonical document has front matter naming its subject, role, state, and
relations. Dated evidence remains under `evidence/`; documents interpret it but
do not duplicate raw records.

## 6. Benchmark and Evidence Lanes

`benchmark.py` becomes a tool-owned comparison runner. The benchmark workload
and its candidate matrix remain useful, but they are evidence for route
admission, not the runtime's source of truth.

The retained evidence classes are:

1. `evidence/benchmarks/`: candidate comparisons, M1 runtime summaries and
   authorized M2-M5 validation summaries;
2. `evidence/verification/`: publication, local matrix, security and cleanup
   receipts;
3. generated local output: ignored and disposable, never promoted merely
   because it exists.

## 7. ETHOS Adoption Decision

The repository **should become an ETHOS adopter** after the topology exists.
It should use a Python base profile and GitLab hosted projection, while retaining
all domain policy, route, evidence, and adapter semantics as repository-owned
truth.

ETHOS owns only the governance loop:

```text
orient -> status -> plan -> prove -> land -> publish
```

The repository owns its domain gates:

- policy and redaction contract;
- system schema validation;
- Python 3.12/3.13/3.14 matrix;
- Firecrawl provenance;
- authorized runtime validation and teardown;
- GitLab hosted observation, distinct from local proof.

Adoption must be fail-closed. The present `ethos adopt --dry-run` reports
`adoption_conflict` paths, so no apply is permitted until a fresh dry-run against
the reorganized repository produces only the reviewed ETHOS binding, governance,
OpenSpec, and documentation kernel files. ETHOS source code is not vendored;
the repository does not take a runtime dependency on ETHOS.

## 8. Migration Strategy

1. Establish package, system, tools, docs and evidence roots; move files without
   changing policy behavior.
2. Split existing root modules into the stated units, update imports, console
   entry point and tests, then remove flat compatibility facades in the same
   reviewed change because no external API has been promised.
3. Encode the existing receipt and bridge contracts as schemas; make schema
   checks part of local and hosted proof.
4. Recast benchmark scripts as tools and preserve only curated body-redacted
   evidence. Keep ignored runtime output outside tracked evidence.
5. Install owner CI scripts and reduce `.gitlab-ci.yml` to projection only.
6. Write canonical documentation indexes, decisions and references; move dated
   material to evidence or history according to its lifecycle state.
7. Run an ETHOS Python dry-run, then GitLab overlay dry-run. Reconcile only
   expected write-plan files; do not overwrite repository-owned contracts.
8. Apply adoption only with explicit authorization, an exact HEAD, a reviewed
   rollback list, and a green local proof. Hosted CI remains a separate claim.

## 9. Acceptance

The reorganization is accepted only when all are true:

1. No domain implementation module remains at repository root; imports begin
   from `web_ingestion` and the console command is the only user entry point.
2. All system declarations and receipt/bridge artifacts validate against tracked
   schemas.
3. Existing safety behavior is preserved: private targets, redirect pivots,
   robots denial, bad MIME, duplicate promotion, result-target drift and page
   budget overruns remain fail-closed.
4. The locked Python 3.12, 3.13 and 3.14 matrix is green; shell, Gitleaks,
   documentation and schema gates are green.
5. The explicit Firecrawl runtime validation completes its authorized workload,
   provenance, private-loopback recovery and zero-resource teardown checks.
6. `ethos adopt` dry-runs cleanly and the adopted repository's `orient`,
   `status`, `plan`, and `prove` produce repository-scoped evidence.
7. `main` remains protected, local and remote evidence are reported separately,
   and hosted CI is never claimed green before an eligible runner executes it.

## 10. Non-Goals

- No standing crawler or Firecrawl daemon.
- No arbitrary public or private target access.
- No body persistence or RAG corpus synchronization.
- No MCP, default Agent, Hermes or Open WebUI integration.
- No copying of ETHOS's product topology, packages, claims store or internal
  state into this repository.
