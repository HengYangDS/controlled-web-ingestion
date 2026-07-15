---
subject: controlled-web-ingestion:governance-closeout-2026-07-15
role: evidence
state: active
relations:
  evidence: evidence/verification/2026-07-15-controlled-web-ingestion-governance-closeout.json
  decision: docs/decisions/0002-delivery-train-boundary.md
  admission: docs/reference/admission.md
---

# Governance Closeout — 2026-07-15

## Facts

The local release root now distinguishes `main`,
`accepted/controlled-web-ingestion`, `candidate/controlled-web-ingestion`, and
an owned `work/` lane. This repairs the earlier role collision without changing
the ingestion runtime, target policy, persistence model, or user-facing
surface.

The dated local matrix, explicit Firecrawl runtime receipt, ETHOS adopter
proof, hosted GitLab pipeline, and protected-branch merge are retained as
separate historical facts. GitHub is now an independent complete repository
and CI/CD plane, so no GitHub Actions fact exists for this earlier closeout
head. Its identifiers and limits are listed in the machine receipt for this
closeout. In particular, the explicit runtime proof was not re-run in this
governance change: the runtime implementation and authorized workload remain
unchanged, while the changed CI bootstrap test affects delivery verification
rather than the runtime route.

On 2026-07-15, three unauthenticated health probes and one SSH transport probe
to the configured GitLab service timed out. No authenticated project, runner,
pipeline, merge-request, or branch query could therefore establish current
remote state. No runner was registered, changed, reused, or removed.

## Conclusions

The repository has a locally auditable delivery train and a bounded governance
closeout. It remains a portable Controlled Web Ingestion capability, not a
standing scraping service. Firecrawl remains an on-demand, disposable,
loopback-only implementation behind the sole `web-ingest` interface.

Historical GitLab success and the historical protected-main merge prove their
dated events only. They do not establish that an eligible runner is available
today, that the local bootstrap commit has been published, or that this
closeout work lane has passed hosted CI.

## Unfinished work and external block

The dual-plane model is additionally pending creation and protection of the
GitHub repository. GitLab publication remains blocked externally until the
configured GitLab service is reachable. Before either implementation release,
maintainers must re-read both platforms' repository, protection, and eligible
executor state; push only the reviewed candidate head; observe independent
GitHub Actions and GitLab matrix results; then use each platform's protected
`main` path. The local release root must not be pushed directly.

The completed local OpenSpec carrier is archived into the canonical
governance-closeout specification before candidate integration. Archiving records
that the local governance material is complete; it does not claim remote
publication. The Codex goal remains active because a local proof cannot replace
hosted execution or a protected-branch merge.

## Lessons

1. A framework or adapter cannot define the capability identity. Policy,
   schemas, receipts, and proof boundaries precede runtime convenience.
2. Historical success must be named as historical. A prior runner or pipeline
   is evidence of a past event, not a standing delivery resource.
3. Delivery roles need distinct semantics. A protected release root cannot also
   be the mutable integration root used to mint work lanes.
4. A runner shortage, network outage, or missing hosted repository is an
   external block, not a reason to weaken gates, create a personal permanent CI
   service, or widen authority.
5. Housekeeping is evidence-preserving: only the current-turn bootstrap
   virtual environment and runtime scratch directory were removed after the
   failed preflight; historical receipts and benchmark evidence were retained.
