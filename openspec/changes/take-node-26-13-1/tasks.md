# Tasks

## 1. Node

- [x] 1.1 Declare node 26.13.1 in `.config/mise/config.toml` and lock it again with `mise lock`;
      done when the lock changes only node's entries, keeps `lockfile_version = 3`,
      `mise install --locked node` installs 26.13.1, and every `mise run check` command passes. The
      lock changed only node's entries, for the same three platforms, with checksums equal to Node's
      `SHASUMS256.txt`, and kept `lockfile_version = 3`; `mise install --locked node` installed
      v26.13.1; every `mise run check` command passes, 89 tests included.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and
  OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by
  itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge
  request.
