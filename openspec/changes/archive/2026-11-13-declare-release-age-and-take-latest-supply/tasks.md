# Tasks

## 1. Supply

- [x] 1.1 Declare `minimum_release_age = "0h"` under `[settings]` in `.config/mise/config.toml`;
      done when `mise settings get minimum_release_age` reports `0h` in the repository.
      `mise settings get minimum_release_age` reports `0h` in the lane, where `mise ls-remote uv`
      now ends at 0.13.8.
- [x] 1.2 Declare Ruff 0.17.5 and Prettier 3.10.1 and lock them again with `mise lock`; done when
      only those tools' entries change, Prettier's lock sits in
      `.config/mise/locks/npm-prettier/3.10.1/` with 3.9.10's removed, `lockfile_version = 3` holds
      and `mise install --locked` installs them. The lock changed only the `npm:prettier` and `ruff`
      entries and kept `lockfile_version = 3`; `mise install --locked` installed Ruff 0.17.5 and
      Prettier 3.10.1; the lock directory holds 3.10.1 alone.
- [x] 1.3 Move the uv lock to the latest stable releases; done when `uv lock --check` passes, the
      lock holds no `exclude-newer`, OSV reports no new advisory and every `mise run check` command
      passes. At cutoff 2026-11-13T15:48:09Z the lock moved exactly coverage 7.17.3, humanize
      4.17.0, openai 3.50.0, `pydantic-settings` 2.16.3 and trimesh 5.2.1 of 150 packages;
      `uv lock --check` passes, the lock holds no `exclude-newer`, OSV reports only the base lock's
      scrapy PYSEC-2017-83, and every `mise run check` command passes, 89 tests included.

## Deferred

- uv 0.13.8 with its three GitLab job images. Owner: the repository's maintainer. Next action: ask
  the owner whether the shared runners admit and load the three images, or whether the repository
  freezes on uv 0.13.7. Review date: 2026-11-14.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and
  OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by
  itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge
  request.
