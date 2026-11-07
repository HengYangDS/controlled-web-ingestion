# Tasks

## 1. Projection declaration

- [x] 1.1 Declare both pipelines as `cue` projections of `.config/ci/pipeline.cue` in `.config/checks/ci-projection/policy.toml`, compiled with the repository's locked `cue`, and expose the provider values under `compiled.providers`; done when `ethos lane project --check` conforms, a changed pipeline is reported as drift, `cue fmt` leaves the model unchanged; the proof's `controlled-web-ingestion-ci-projection` gate runs `tools/ci/project.py --check`. Under 0.2.0-beta.6, `ethos lane project --check` conforms; a copy with one line appended to `.gitlab-ci.yml` is blocked as `generated_projection_drift:.gitlab-ci.yml`; `cue fmt` leaves the model unchanged.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
