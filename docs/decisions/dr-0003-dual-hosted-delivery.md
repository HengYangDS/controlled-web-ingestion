---
subject: controlled-web-ingestion:dual-hosted-delivery
role: decision
state: canonical
decision_id: DR-0003
decision_status: accepted
relations:
  canonical_for: GitHub and GitLab independent repository and CI/CD planes
  governed_by: docs/decisions/dr-0001-ethos-adopter-boundary.md
  delivery_train: docs/decisions/dr-0002-delivery-train-boundary.md
---

# DR-0003: Operate GitHub and GitLab as independent delivery planes

## Context

Controlled Web Ingestion is published through two forges, GitHub and GitLab,
and each forge has its own review, branch protection and hosted CI.

## Decision

GitHub and GitLab are each complete, first-class repositories for Controlled
Web Ingestion. Each carries source, policy, schemas, documentation, evidence,
the controlled GitHub Actions or GitLab CI projection, and its own protected
publication path. GitHub is not a source snapshot, a passive mirror, or a
fallback for GitLab; GitLab retains the same standing.

Both platforms execute the same repository-owned verification commands. Their
hosted observations remain independent: a successful GitHub Actions run does
not prove GitLab CI, and a successful GitLab pipeline does not prove GitHub
Actions. The explicit Firecrawl runtime validation remains a separate local
acceptance gate and is not converted into generic hosted CI on either platform.

Delivery follows one path:

1. An owned Work Lane.
2. A reviewed candidate.
3. A GitHub pull request with GitHub Actions.
4. A GitLab merge request with GitLab CI.
5. Protected `main` on each platform.

The local ETHOS train is the authoring and integration control. It does not
privilege either hosted forge. Before an implementation release, the candidate
head must be identical on both remotes; each platform's protected `main` must
advance only through its own reviewed change path and current hosted evidence.

## Alternatives Rejected

- **GitHub as snapshot/mirror:** rejected because it hides CI/CD and protection
  drift behind a shallow copy.
- **One forge as the sole CI authority:** rejected because it leaves the other
  stated delivery plane unverified.
- **Cross-platform auto-push or auto-merge:** rejected because an unavailable
  or compromised forge must not cause the other forge to publish without its
  own review and protected-branch controls.

## Consequences and Boundary

- `.github/workflows/verify.yml` and `.gitlab-ci.yml` are thin, independent
  host projections over the same owner scripts under `tools/ci/`, generated
  from the one pipeline model in `.config/ci/pipeline.cue`.
- GitHub action references are pinned to reviewed commit identifiers and run
  with least-privilege `contents: read` permissions.
- Each publication receipt names platform, repository identity, source head,
  candidate head, workflow or pipeline identifier, required jobs, outcome,
  timestamp, branch-protection observation, and limitations.
- A platform outage is an external block for that platform. It is not a reason
  to weaken gates, create a personal permanent runner, or substitute historical
  proof.
- GitLab CI runs only on the project-locked runner pair `ci-p473-linux-arm64-docker-review` and
  `ci-p473-linux-arm64-docker-protected` on the dedicated CI Linux ARM64 host. Ref protection
  selects the runner, and every job runs in a digest-pinned image from the runners' allowlist,
  without privileged mode or the host Docker socket. This pair is the declared GitLab runner
  contract while the organization offers no instance or group runner, and such a runner replaces
  it. A runner in a person's login session, such as a shell executor on a workstation account, is
  a personal runner and is not eligible.

## Evidence and Revisit

Revisit only when one platform's branch-protection model, hosted runner
contract, repository ownership, or security boundary changes. A convenience
request to reduce independent verification is insufficient.
