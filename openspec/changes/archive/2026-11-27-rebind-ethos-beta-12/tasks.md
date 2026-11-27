# Tasks

## 1. Runtime

- [x] 1.1 Bind the repository family to the 0.2.0-beta.12 runtime, installed with native Mise from
      the release's own declaration, whose platform checksums are checked against the release's
      `SHA256SUMS` and whose installed runtime's manifest names the tagged commit, through its
      console's `hook install`, keeping 0.2.0-beta.11 as the rollback; done when CURRENT names the
      0.2.0-beta.12 runtime and ROLLBACK the 0.2.0-beta.11 one, and `ethos status` reports the lane
      ready. The release's declaration (sha256 `094105e2…`) has five platform checksums equal to
      `SHA256SUMS` and the API digests; native Mise installed the macOS archive, whose manifest
      names source commit cdb51d469, the tagged commit; the console's `hook install` passed. CURRENT
      names the 0.2.0-beta.12 runtime `3e6b10f2…` and ROLLBACK the 0.2.0-beta.11 runtime
      `8c663b10…`; `ethos status` reports the lane ready.
- [x] 1.2 Name each gate's provider by its catalog ID in `.ethos/profile.toml`
      (`provider.code-behavior`, `provider.code-static`); done when `ethos status` reports the lane
      ready, the contract test that asserts the two names passes with them, and an executed check
      names neither gate in a `gate_provider_legacy_name` note. The executed readiness under
      0.2.0-beta.12 passed all 17 checks; its notes name neither gate. They name eight gates that
      ETHOS itself declares (configuration, Docs Registry, Markdown links and lint, OpenSpec, prose,
      schemas, source format), which this repository does not declare and cannot rename. The review
      of the lane found that `tests/contract/test_ethos_boundary.py` still asserted the legacy
      names; it now asserts the catalog IDs, and its four tests pass.
- [x] 1.3 Name 0.2.0-beta.12 as the pin floor in the README's frozen status and state that the
      repository takes ETHOS binds only, no supply Change; done when the documentation gates pass.
      The README's status names ETHOS 0.2.0-beta.12 and ETHOS binds only; the format check and the
      documentation gates pass.

## Workflow follow-up

- Archive this Change and prove the archived head once.
- Publish the proposal, wait for both forges' review jobs, land, publish `dev` and `main`, and read
  the protected jobs back; then retire the lane.
