# Tasks

## 1. Peer-free shared content

- [x] 1.1 Remove both `forge_repository` lines from `.ethos/release.toml`; done when `ethos status` is ready and the publication topology loads both peers without a gap. Under 0.2.0-beta.5 `ethos status` is ready, and the publication probes for `gitlab` and `github` report a ready topology with both peers and are ready to publish.
- [x] 1.2 Build the target-policy tests' private-space example at run time; done when the tests pass and no tracked file outside `evidence/` names a private-space literal. The 8 tests in `tests/unit/test_policy_and_staging.py` pass, and the paradigm's private-address pattern matches no tracked file outside `evidence/`.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
