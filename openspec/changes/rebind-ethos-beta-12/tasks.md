# Tasks

## 1. Runtime

- [ ] 1.1 Bind the repository family to the 0.2.0-beta.12 runtime, installed with native Mise from
      the release's own declaration, whose platform checksums are checked against the release's
      `SHA256SUMS` and whose installed runtime's manifest names the tagged commit, through its
      console's `hook install`, keeping 0.2.0-beta.11 as the rollback; done when CURRENT names the
      0.2.0-beta.12 runtime and ROLLBACK the 0.2.0-beta.11 one, and `ethos status` reports the lane
      ready.
- [ ] 1.2 Name each gate's provider by its catalog ID in `.ethos/profile.toml`
      (`provider.code-behavior`, `provider.code-static`); done when `ethos status` reports the lane
      ready and an executed proof notes no `gate_provider_legacy_name`.
- [ ] 1.3 Name 0.2.0-beta.12 as the pin floor in the README's frozen status and state that the
      repository takes ETHOS binds only, no supply Change; done when the documentation gates pass.

## Workflow follow-up

- Archive this Change and prove the archived head once.
- Publish the proposal, wait for both forges' review jobs, land, publish `dev` and `main`, and read
  the protected jobs back; then retire the lane.
