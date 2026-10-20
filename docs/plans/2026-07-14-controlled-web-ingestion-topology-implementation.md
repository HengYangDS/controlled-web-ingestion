---
subject: web-ingestion:topology-implementation
role: plan
state: active
relations:
  implements: docs/architecture/controlled-web-ingestion-topology.md
  supersedes: docs/plans/2026-07-14-web-ingestion-m2-m5-implementation.md
---

# Controlled Web Ingestion: Topology Implementation Plan

> **For agentic workers:** Execute in this isolated worktree, review each gate before continuing, and update each checkbox only after its recorded verifier exits successfully.

**Goal:** Convert the publication from a flat framework-admission benchmark into the portable, policy-bound **Controlled Web Ingestion** capability described by the approved topology, then adopt ETHOS's Python and GitLab governance loop without importing ETHOS product complexity.

**Architecture:** A single installable `web_ingestion` package owns all runtime contracts and the `web-ingest` console command. Declarative repository truth moves into `system/`; operational scripts into `tools/`; benchmark code becomes an evidence lane; tests become unit, contract and integration layers. ETHOS remains an external governance overlay; repository-owned policy, schemas, evidence and runtime gates remain authoritative.

**Tech stack:** Python `>=3.12`, `uv --locked`, stdlib `unittest`, JSON Schema validation implemented without a new runtime dependency, Trafilatura, disposable loopback Firecrawl Compose runtime, GitLab CI, ETHOS CLI.

## Global constraints

- The canonical distribution and GitLab project path are `controlled-web-ingestion`; title case is prose only.
- Preserve `requires-python >=3.12` without an upper bound and prove 3.12, 3.13 and 3.14 separately.
- Never persist body, HTML, Markdown, raw response, credentials, private targets or account state in committed code, fixtures, receipts, evidence or Git history.
- Retain the pre-existing semantic safety gates: public target and redirect admission, robots, MIME, bounded page/time budgets, body-redacted receipt, duplicate-promotion refusal, Firecrawl result re-admission and output-page bound.
- `web-ingest` is the sole user-facing interface. Do not retain a root compatibility facade and do not expose raw Firecrawl as MCP, an Agent tool, Hermes/Open WebUI integration or a direct RAG sink.
- Firecrawl stays on demand, disposable and loopback-only. Do not change Docker daemon configuration, add a registry mirror, reuse a shared listener/service, or turn runtime validation into a generic CI job.
- `main` is protected. Work only on `work/controlled-web-ingestion-topology`; create an MR and distinguish local proof, hosted CI observation, and merge evidence.
- Never weaken a required gate merely because a GitLab runner is unavailable.

## Acceptance map

| Design acceptance | Delivering tasks | Fresh proof |
| --- | --- | --- |
| No root implementation / only console entry point | 2–4 | import guard plus `web-ingest --help` |
| System truth and artifacts schema-validate | 5–6 | schema validator over policy, projections, receipts, bridge and evidence |
| Existing safety behavior preserved | 2–4 | migrated 52+ unit/contract tests |
| Python 3.12/3.13/3.14 plus shell/security/docs/schema gates | 7, 11 | owner CI scripts locally and hosted pipeline |
| Authorized Firecrawl runtime / teardown proof | 8 | explicit runtime tool receipt only |
| Clean ETHOS adopt dry-run and repository-scoped loop | 9 | reviewed write plan, head-bound apply, orient/status/plan/prove |
| Protected main and honest hosted status | 10–12 | MR and pipeline evidence |

---

### Task 1: Record the approved topology as active work

**Files:**

- Modify: `docs/architecture/controlled-web-ingestion-topology.md`
- Create: `docs/plans/2026-07-14-controlled-web-ingestion-topology-implementation.md`
- [x] Change design metadata from `proposed` to `active` and link this implementation plan.
- [x] State acceptance mapping, exclusions, exact branch boundary, verifier classes and no-gate-weakening rule.
- [x] Commit the document-only approval boundary before moving source files.

**Verifier:** `git diff --check` and a clean `git status --short` after commit.

### Task 2: Create the installable runtime package without changing behavior

**Files:**

- Create: `src/web_ingestion/__init__.py`
- Create: `src/web_ingestion/contracts.py`
- Create: `src/web_ingestion/policy.py`
- Create: `src/web_ingestion/transport.py`
- Create: `src/web_ingestion/controller.py`
- Create: `src/web_ingestion/staging.py`
- Create: `src/web_ingestion/bridge.py`
- Create: `src/web_ingestion/adapters/__init__.py`
- Create: `src/web_ingestion/adapters/static.py`
- Create: `src/web_ingestion/adapters/firecrawl.py`
- Create: `tests/unit/test_import_boundary.py`
- Modify: `pyproject.toml`

**Interfaces:**

- `web_ingestion.contracts` exports `IngestionError`, `IngestionRequest`, `RawHttpResponse`, `HttpFetch`, `IngestionOutcome`.
- `web_ingestion.policy` exports `TargetPolicy`, `TargetDecision`, `RobotsDecision`, `PromotionError`, URL/robots/MIME policy functions.
- `web_ingestion.transport.SafeHttpClient` has the existing bounded-fetch contract.
- `web_ingestion.controller.IngestionController` consumes the contracts, policy, transport and adapters.
- `web_ingestion.staging.StageStore` owns staging/promotion.
- `web_ingestion.bridge.RagBridge` remains sinkless by default.
- [ ] Write a failing import-boundary test that imports each public package unit and asserts no root implementation module exists.
- [ ] Run that test and record its expected import failure before moving code.
- [ ] Move code by responsibility, preserving public names and dependency direction; use package-relative imports only.
- [ ] Set `[build-system]` to Hatchling, package discovery to `src`, package name to `controlled-web-ingestion`, and entry point `web-ingest = "web_ingestion.cli:main"`.
- [ ] Re-run migrated unit/contract suites and `web-ingest --help` using `uv run --locked`.
- [ ] Remove all root-level runtime modules in the same change; do not introduce shims.

**Verifier:** `uv run --locked python -m unittest discover -s tests/unit -v`, `uv run --locked python -m unittest discover -s tests/contract -v`, `uv run --locked web-ingest --help`.

### Task 3: Migrate CLI, adapter and supply-chain ownership

**Files:**

- Create: `src/web_ingestion/cli.py`
- Create: `src/web_ingestion/supply_chain/__init__.py`
- Create: `src/web_ingestion/supply_chain/provenance.py`
- Create: `src/web_ingestion/supply_chain/ghcr_archive.py`
- Create: `src/web_ingestion/supply_chain/ghcr_ranges.py`
- Create: `src/web_ingestion/supply_chain/ghcr_registry.py`
- Create: `tools/runtime/firecrawl-isolated-benchmark.sh`
- Create: `tools/runtime/validate-authorized-workloads.sh`
- Create: `tools/runtime/verify-firecrawl-provenance.py`
- Create: `tools/supply-chain/import-pinned-firecrawl-images.py`
- Test: `tests/contract/test_cli.py`, `tests/unit/test_firecrawl_client.py`, `tests/unit/test_supply_chain_*.py`
- [ ] Write failing imports and executable-path tests for `web_ingestion.cli`, adapter modules and supply-chain modules.
- [ ] Move Firecrawl client code to `adapters/firecrawl.py`, static extractor to `adapters/static.py`, and supply-chain utilities under `supply_chain/`.
- [ ] Update all runtime/supply-chain scripts to import package modules through the locked environment; retain only fixed runner invocation, no generic shell execution.
- [ ] Preserve command semantics (`ingest`, `promote`, `prepare-rag`) and body-redaction behavior.
- [ ] Move scripts from `scripts/` to their tool owners and update test references.

**Verifier:** full test discovery, both shell syntax checks and `web-ingest ingest --help`.

### Task 4: Separate benchmark evidence from controlled runtime

**Files:**

- Create: `tools/benchmark/run_framework_comparison.py`
- Create: `tests/integration/test_benchmark_lane.py`
- Move: `benchmark.py` to `tools/benchmark/run_framework_comparison.py`
- Move: `cases.json` to `system/projections/framework-comparison-cases.json`
- Modify: README and benchmark documentation references
- [ ] Write a failing integration test that imports the comparison runner from the tools lane and asserts it writes only a body-redacted record.
- [ ] Move candidate-comparison logic and update imports to use package policy/adapters where applicable.
- [ ] Ensure the runtime package does not import benchmark tooling.
- [ ] Retain Firecrawl, Crawl4AI, Crawlee, Scrapy plus Trafilatura and Jina Reader strictly as adapter/baseline candidates.

**Verifier:** integration benchmark-lane test and a source-boundary scan showing no `benchmark` import under `src/web_ingestion/`.

### Task 5: Move reviewed repository truth under `system/`

**Files:**

- Move: `policy.json` to `system/policies/ingestion-policy.json`
- Move: `ops/web-ingestion-authorized-workloads.json` to `system/policies/authorized-workloads.json`
- Move: `ops/web-ingestion-routing.json` to `system/projections/routing.json`
- Move: `ops/firecrawl-isolated-compose.yaml` to `system/projections/firecrawl-isolated-compose.yaml`
- Move: `ops/firecrawl-images.json` to `system/supply-chain/firecrawl-images.json`
- Move: `ops/firecrawl-provenance.json` to `system/supply-chain/firecrawl-provenance.json`
- Create: `tests/contract/test_system_declarations.py`
- [ ] Write failing contract tests for every declared file and its required no-secret/no-body fields.
- [ ] Move declarations unchanged except for the new canonical project/CLI identifiers.
- [ ] Update package code, tools and docs to resolve system files from the repository root explicitly; no current-working-directory ambiguity.
- [ ] Delete `ops/` and root `policy.json` after all callers and tests use `system/`.

**Verifier:** contract declaration tests plus `git grep -nE 'policy.json|ops/' -- ':!docs/history/**'` returning only deliberate migration-history references.

### Task 6: Add schemas and fail closed on persisted artifacts

**Files:**

- Create: `system/schemas/ingestion-policy.schema.json`
- Create: `system/schemas/authorized-workloads.schema.json`
- Create: `system/schemas/routing.schema.json`
- Create: `system/schemas/stage-receipt.schema.json`
- Create: `system/schemas/promotion-receipt.schema.json`
- Create: `system/schemas/bridge-manifest.schema.json`
- Create: `system/schemas/evidence.schema.json`
- Create: `tools/ci/validate_schemas.py`
- Create: `tests/contract/test_schema_contracts.py`
- [ ] Write failing tests for a valid staged/promotion/bridge artifact and one recursive forbidden-field counterexample for each artifact type.
- [ ] Implement a narrow local JSON-Schema validator for the used Draft 2020-12 subset: object, array, string, integer, number, boolean, required, properties, items, enum, const, pattern, minimum, maximum, additionalProperties and recursive `not`-forbidden keys.
- [ ] Validate all system declarations and committed evidence with their tracked schema.
- [ ] Make stage/promotion/bridge writers validate before persistence so invalid artifacts never become receipts.

**Verifier:** `uv run --locked python tools/ci/validate_schemas.py` and contract schema tests.

### Task 7: Establish owner CI commands and test topology

**Files:**

- Create: `tools/ci/run_tests.py`
- Create: `tools/ci/check_documentation.py`
- Create: `tools/ci/check_source_topology.py`
- Create: `tools/ci/run_security_checks.sh`
- Modify: `.gitlab-ci.yml`
- Move tests into: `tests/unit/`, `tests/contract/`, `tests/integration/`
- [ ] Write a failing source-topology test that rejects root implementation modules, `scripts/`, `ops/`, untracked schema roots, and package-to-tool imports.
- [ ] Relocate tests by layer without reducing coverage; update discovery and module names.
- [ ] Implement owner scripts that perform tests, shell syntax, schema, docs and security checks. `.gitlab-ci.yml` must only select Python versions and call these scripts.
- [ ] Preserve the three-version required matrix and Firecrawl runtime omission rationale.

**Verifier:** each owner command locally; inspect `.gitlab-ci.yml` to confirm no duplicated inline validation logic.

### Task 8: Re-run explicit runtime proof

**Files:**

- Modify: `tools/runtime/validate-authorized-workloads.sh`
- Modify: `docs/reference/runtime-validation.md`
- Create: `evidence/verification/2026-07-14-controlled-web-ingestion-runtime-validation.json`
- [ ] Update paths and the project/CLI identity, preserving exact authorized workloads and teardown assertions.
- [ ] Run the explicit on-demand runtime validator only after provenance preflight succeeds.
- [ ] Store only the redacted summary and resource cleanup outcome under `evidence/verification/`.
- [ ] If runtime cannot be repeated because its documented external precondition is absent, record the exact blocker and leave the runtime gate open; never fabricate a success result.

**Verifier:** validator exit code, redacted evidence inspection, and zero-resource cleanup checks.

### Task 9: Adopt ETHOS as external governance, not runtime ownership

**Files:**

- Create only reviewed ETHOS-generated binding/governance/OpenSpec files under `.ethos/` and `openspec/`
- Create: `docs/decisions/0001-ethos-adopter-boundary.md`
- Create: `docs/start/adopter-governance.md`
- Test: `tests/contract/test_ethos_boundary.py`
- [ ] Write a failing boundary test stating that the package has no ETHOS runtime import and no copied ETHOS product package.
- [ ] Create the decision record: ETHOS owns `orient -> status -> plan -> prove -> land -> publish`; Controlled Web Ingestion owns policy, adapter, schema, runtime and evidence truth.
- [ ] Run `ethos adopt --dry-run --root <worktree>` for Python, save exact output, then run GitLab overlay dry-run.
- [ ] Review every proposed write; reject conflicts and any overwrite of repository-owned domain documents.
- [ ] With clean dry-runs, a pinned HEAD and rollback list, apply only the reviewed adoption plan; run `ethos orient`, `status`, `plan` and `prove` with the same `--root`.

**Verifier:** clean dry-run output, tracked adoption delta, ETHOS loop evidence, source-boundary test.

### Task 10: Create the documentation and evidence kernel

**Files:**

- Create: `docs/start/README.md`
- Create: `docs/decisions/0000-controlled-web-ingestion-position.md`
- Create: `docs/evidence/README.md`
- Create: `docs/reference/cli.md`
- Create: `docs/reference/contracts.md`
- Create: `docs/reference/runtime-validation.md`
- Create: `docs/history/README.md`
- Move legacy benchmark narratives to `docs/history/` when superseded
- Modify: `README.md`, `docs/research-contract.md`, `docs/PUBLICATION.md`
- [ ] Write canonical front matter for all kernel documents (`subject`, `role`, `state`, `relations`).
- [ ] State the controlled-acquisition identity in README; retain Research / Knowledge Systems contract without calling the repository a benchmark product.
- [ ] Document CLI, schemas, evidence classes, adapter boundary, runtime gate and ETHOS adoption boundary.
- [ ] Add a concise migration note linking historical benchmark records without rewriting or deleting evidence.

**Verifier:** documentation owner check and link/path scan.

### Task 11: Obtain complete local proof

**Files:**

- Create: `evidence/verification/2026-07-14-controlled-web-ingestion-local-proof.json`
- Modify: `evidence/verification/README.md` if generated by Task 10
- [ ] Execute the locked Python matrix with exact interpreters 3.12, 3.13, and 3.14 through the owner CI command.
- [ ] Execute schema, source topology, documentation, shell syntax and Gitleaks owner commands.
- [ ] Run `git diff --check`, inspect tracked evidence for forbidden persistence fields, and verify no dirty runtime output is staged.
- [ ] Record command, timestamp, exit status, test count and limitation in a body-redacted local-proof receipt.

**Verifier:** all owner commands exit zero; receipt validates against `evidence.schema.json`.

### Task 12: Rename/publish GitLab project through protected delivery

**Files:**

- Modify only remote GitLab project metadata after local proof is green.
- [ ] Use live GitLab API evidence to verify project ID, namespace, current protection and branch head.
- [ ] Rename display name and canonical path to `controlled-web-ingestion` under the confirmed Research / Knowledge Systems namespace; do not move it to a historical/non-authoritative group.
- [ ] Push the work branch, create or update an MR with the decision, local proof and hosted-CI distinction.
- [ ] Observe each GitLab matrix job. A runner scheduling failure is infrastructure evidence, not passing CI.
- [ ] Merge only after an eligible runner executes every required job successfully and GitLab permits the protected-branch merge.

**Verifier:** GitLab project API, MR API, pipeline/jobs API and protected-main commit evidence.

### Task 13: Evidence-led closeout and goal completion

**Files:**

- Create: `evidence/verification/2026-07-15-controlled-web-ingestion-governance-closeout.json`
- Create: `docs/evidence/chronicle/2026-07-15/governance-closeout.md`
- Create: `docs/history/2026-07-15-topology-migration.md`
- Create: `docs/reference/admission.md`
- [x] Reconcile each acceptance-map row against a command, API observation, or evidence path and label it `verified`, `historical`, `blocked`, or `not-run`.
- [x] Separate local proof, runtime proof, ETHOS proof, hosted CI, protected-main publication, and current runner reachability into independent evidence classes.
- [x] Record lessons: adapter products cannot own the capability identity; policy/schema/evidence boundary precedes runtime convenience; runner shortage cannot be solved by weakening gates.
- [ ] Mark the Codex goal complete only after fresh hosted verification has passed and protected `main` contains this closeout merge.

**Verifier:** closeout receipt schema validation, clean proven Work Lane, current GitLab `main` evidence, and final acceptance audit.
