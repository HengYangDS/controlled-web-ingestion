## Why

GitLab CI for this project runs on runner 129. It is a macOS shell executor in the owner's login
session, and it uses the owner's Homebrew interpreters. DR-0003 forbids creating a personal
permanent runner, and the delivery-governance spec says that personal runners do not substitute
for platform evidence. Yet the organization offers no instance or group runner to
`knowledge-systems`.

The owner's other governed projects use a declared pattern instead. Each has a project-locked pair
of docker-executor runners on the dedicated CI Linux ARM64 host, split by ref protection, and its
jobs run in digest-pinned images.

## What Changes

- `.gitlab-ci.yml` runs every job in a digest-pinned image: `ghcr.io/astral-sh/uv:0.13.1` with
  Python 3.12, 3.13 or 3.14 on Debian trixie, and `ghcr.io/gitleaks/gitleaks:v8.30.1`. Workflow
  rules route protected-ref pipelines to the `ci-linux-arm64-container-protected` runner tag and
  every other pipeline to `ci-linux-arm64-container`.
- DR-0003 and the delivery-governance spec define the eligible GitLab runner. The declared pair
  qualifies. A runner in a person's login session remains a personal runner.
- Outside the repository, the pair `ci-p473-linux-arm64-docker-review` and
  `ci-p473-linux-arm64-docker-protected` is registered on the CI host with an image allowlist, no
  privileged mode and no host Docker socket. Runner 129 is retired after the pair has run.

## Evidence Boundary

Local evidence: strict OpenSpec validation, the repository gates, the ETHOS proof, and the CI job
commands run in the same images on the local OrbStack engine. Hosted evidence: the first GitLab
pipelines on the new runners.

## Non-goals

- No change to GitHub Actions.
- No organization instance or group runner. When one exists, it replaces the pair.
