# Web-Ingestion M2–M5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 交付一个受策略约束的按需 Web-Ingestion 入口、可验证的 Firecrawl 运行治理、真实公开工作负载证据与默认关闭的 RAG bridge。

**Architecture:** `web_ingest.py` 是唯一用户入口，控制器将请求准入、受控 HTTP preflight、路由、质量和 receipt 固化在 `web_ingestion.py`。Firecrawl 只在 CLI 内部借助现有 disposable loopback runner 运行；RAG 通过独立 bridge contract 处理，不触碰现有 RAG 或 UI。

**Tech Stack:** Python 3.12–3.14、uv locked dependencies、Trafilatura、Docker Compose、Homebrew Redis/RabbitMQ、官方 GHCR images。

## Global Constraints

- 只访问已有基准中已授权的公开 URL：`https://example.com/`、`https://quotes.toscrape.com/js/`、`https://quotes.toscrape.com/`。
- 不安装新的系统软件；不复用 `nomad_redis`、既有 Postgres、既有容器或 listener。
- 不改变 Docker daemon、不添加 registry mirror、不注册 MCP/默认 Agent/Hermes/Open WebUI、不直写现有 RAG。
- 结果、stage、promotion、bridge receipt 均不得保存正文、HTML、Markdown 或 raw response。
- 工作区不是 Git repository；每个任务以命令、测试和 evidence 文件代替 commit 证明。

---

### Task 1: Request and safe-transport contract

**Files:**
- Create: `experiments/web-ingestion-benchmark/web_ingestion.py`
- Create: `experiments/web-ingestion-benchmark/tests/test_web_ingestion.py`
- Modify: `experiments/web-ingestion-benchmark/admission.py`

**Interfaces:**
- Produces `IngestionRequest`, `SafeHttpClient`, `IngestionController`, `IngestionOutcome`.
- `IngestionRequest(url, purpose, mode, max_pages, timeout_seconds, engine)` rejects absent purpose, unsupported mode, bad budgets and invalid timeout.
- `SafeHttpClient.fetch()` validates each redirect target before connecting and returns only in-memory bytes plus headers/redirect chain.

- [x] Write failing tests for request validation, redirect-to-private rejection, robots denial, content-type denial, and duplicate rejection.
- [x] Run `UV_PROJECT_ENVIRONMENT=<temp> uv run --locked python -m unittest tests.test_web_ingestion -v`; confirm failures name missing controller/types.
- [x] Implement minimal request validation and no-redirect HTTP loop using `validate_target` before each request.
- [x] Implement robots handling with 404-as-no-rules and transport-error deny for recursive crawl.
- [x] Run the focused suite until green.

### Task 2: Controlled routes and staging receipts

**Files:**
- Modify: `web_ingestion.py`
- Modify: `admission.py`
- Modify: `tests/test_web_ingestion.py`
- Create: `ops/web-ingestion-routing.json`

**Interfaces:**
- `IngestionController.ingest(request, stage_root)` returns an `IngestionOutcome` with a stage receipt path.
- Static route uses safe transport plus Trafilatura; browser/crawl route requires an explicit loopback Firecrawl endpoint.
- Stage records contain `request_id`, `purpose`, `route`, `quality`, `redirect_chain`, `dedupe_decision`; no body fields.

- [x] Add failing tests showing static extraction stages a receipt with no body and duplicate content cannot promote.
- [x] Add route config and controller route selection: static → `trafilatura`; browser/crawl → `firecrawl`.
- [x] Implement in-memory extraction, content digest, quality metrics, and content-digest duplicate detection.
- [x] Tighten `StageStore.promote` to reject a duplicate or a receipt lacking required operational fields.
- [x] Run focused tests and then full local suite.

### Task 3: Unique CLI and Firecrawl runtime provenance gate

**Files:**
- Create: `web_ingest.py`
- Create: `scripts/verify-firecrawl-provenance.py`
- Modify: `scripts/firecrawl-isolated-benchmark.sh`
- Modify: `ops/firecrawl-provenance.json`
- Create: `tests/test_web_ingest_cli.py`
- Create: `tests/test_firecrawl_provenance.py`

**Interfaces:**
- `web_ingest.py ingest ...` requires `--url --purpose --mode --max-pages --timeout-seconds --stage-root`.
- Firecrawl mode internally re-enters through `firecrawl-isolated-benchmark.sh -- <command>`; users never call raw API directly.
- Provenance verifier exits 0 only when reviewed manifest data, expected tags, `linux/arm64`, and recorded local image IDs agree.

- [x] Write CLI/parser and verifier failing tests.
- [x] Extend runner with command-vector mode while preserving default benchmark behavior and trap cleanup.
- [x] Implement verifier and add it before Compose startup.
- [x] Implement CLI `ingest`, `promote`, `prepare-rag`, and internal attached-Firecrawl subcommand.
- [x] Run focused tests, Bash syntax check, Compose config validation, and complete unit suite.

### Task 4: Independent RAG bridge

**Files:**
- Create: `rag_bridge.py`
- Create: `tests/test_rag_bridge.py`
- Modify: `web_ingest.py`

**Interfaces:**
- `RagBridge.prepare(promoted_receipt, explicit_confirmation=True)` emits a body-redacted bridge manifest.
- `RagBridge.deliver_from_memory(promoted_receipt, content, sink, explicit_confirmation=True)` validates digest and invokes an explicit adapter only.
- Default CLI exposes only `prepare-rag`; it has no real RAG sink.

- [x] Write failing tests for unpromoted/no-confirmation/digest-mismatch rejection and one recording sink success case.
- [x] Implement bridge and manifest contract.
- [x] Add CLI preparation command; do not add a default delivery command or a network sink.
- [x] Run bridge tests and full suite.

### Task 5: M3 workload, recovery, and closeout evidence

**Files:**
- Create: `ops/web-ingestion-authorized-workloads.json`
- Create: `scripts/web-ingestion-m2-m5-validate.sh`
- Create: `docs/benchmarks/2026-07-14-web-ingestion-m2-m5-runbook.md`
- Create: `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-validation.json`
- Update: `docs/benchmarks/2026-07-14-web-ingestion-firecrawl-m1-closeout.md`

**Interfaces:**
- Validation script runs static, browser, crawl, duplicate, promotion, bridge preparation, provenance check and deliberately failing Firecrawl child command.
- It emits only redacted summaries and verifies zero benchmark containers, volumes, networks, ports, and project virtualenvs on exit.

- [x] Create public-workload allowlist with exact URLs and purposes.
- [x] Implement validator with a temporary stage root and temporary virtualenv; write receipt summaries only.
- [x] Execute the validator and inspect output for static/browser/crawl success, duplicate rejection, promotion/bridge success, recovery cleanup, and no secrets.
- [x] Run full 3.12/3.13/3.14 locked matrix and static scans.
- [x] Update runbook and final decision with observed evidence and residual limits.

## Self-Review

- M2 single entrance: Tasks 1–3.
- M3 provenance, resources, real public workload, recovery and cleanup: Tasks 3 and 5.
- M4/M5 staging, promotion and independent RAG bridge: Tasks 2 and 4.
- No default RAG/UI/MCP/daemon expansion: global constraints and Tasks 3–5.
- Every production behavior begins with a focused failing test, then a green test.
