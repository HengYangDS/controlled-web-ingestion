# Tasks

## 1. Peer-free shared content

- [ ] 1.1 Remove both `forge_repository` lines from `.ethos/release.toml`; done when `ethos status` is ready and the publication topology loads both peers without a gap.
- [ ] 1.2 Build the target-policy tests' private-space example at run time; done when the tests pass and no tracked file outside `evidence/` names a private-space literal.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
