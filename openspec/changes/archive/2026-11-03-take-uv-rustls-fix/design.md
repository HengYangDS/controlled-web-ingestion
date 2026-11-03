# Design

## Context

`.config/mise/config.toml` declares the uv release and `.config/mise/mise.lock` its checksums.
`.config/ci/pipeline.cue` names the same release as `_uv`, and `tools/ci/project.py` renders
`.github/workflows/verify.yml`, whose setup-uv step installs that version, and `.gitlab-ci.yml`,
whose jobs run one digest-pinned `ghcr.io/astral-sh/uv` image per supported Python, tagged with it.
The contract tests hold both projections to the Mise declaration. On 3 November 2026 the newest
releases were read from Mise, PyPI, the GitHub releases API and GHCR.

## Goals / Non-Goals

**Goals:**

- Move every uv this repository declares to 0.13.7, whose embedded rustls fixes the four
  advisories.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or the Python
  lock.
- Adopting Python 3.15 for the Mise runtime or the CI matrix.

## Decisions

### The fixed release is taken on verified provenance

Mise's default 24-hour minimum release age keeps 0.13.7 out of `latest` until 4 November at
02:45 UTC, and it does not filter an exact pin. The age guards against a release that is
withdrawn or found malicious in its first day. This release's GitHub assets carry build
attestations from astral-sh/uv's release workflow, which `gh attestation verify` accepts, and
`mise lock` records that provenance for each platform. The GHCR images are pinned by index
digest. So the repository takes the fixed release now, as the owner's direction asks, rather
than waiting out the age. ETHOS itself keeps the age for its own supply.

### The lock and the action stay

uv 0.13.7 keeps the lock format, so `uv lock --check` passes on the unchanged `uv.lock`.
setup-uv v10.3.3 is still its newest release, and its `version` input follows `_uv`.

## Risks / Trade-offs

- [uv 0.13.7 changes resolution or installation behavior] → Every `mise run check` command runs
  with the locked uv 0.13.7 before proof, and the hosted matrix runs on 3.12, 3.13 and 3.14.
- [The new images run only on the hosted runners] → Hosted acceptance follows publication of the
  landed head.
