# Proposal

## Why

The owner decided on 13 November 2026 that every governed repository takes the latest stable release
of its supply with a release age of 0 hours, and that the age is declared configuration, in hours.
Mise hides a release younger than 24 hours unless a repository declares otherwise, so until now this
repository waited a day without saying so anywhere. Its declared Ruff 0.17.4 trails 0.17.5, its
Prettier 3.9.10 trails 3.10.1, and its uv lock trails five releases. None of them carries a security
note. ETHOS's own format gate runs Prettier 3.9.10 until its 0.2.0-beta.11; Prettier 3.10.1 accepts
every file that this repository's check covers, so both formatters accept the same tree.

## What Changes

- Declare the release age: `minimum_release_age = "0h"` under `[settings]` in
  `.config/mise/config.toml`.
- Declare Ruff 0.17.5 and Prettier 3.10.1 there and lock them again with native `mise lock`; only
  those tools' lock entries change, Prettier's lock moves to
  `.config/mise/locks/npm-prettier/3.10.1/`, and the lock stays at version 3.
- Move the uv lock to coverage 7.17.3, humanize 4.17.0, openai 3.50.0, `pydantic-settings` 2.16.3
  and trimesh 5.2.1.
- Keep uv at 0.13.7. The pipeline model pins one uv release for Mise and for the three GitLab job
  images, and the GitLab runners admit images by digest; moving uv to 0.13.8 needs those runners to
  admit and load three new images, a change to shared CI that this repository does not make alone.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion contracts are unchanged, so `.openspec.yaml` sets `skip_specs: true`.

## Impact

`.config/mise/config.toml`, `.config/mise/mise.lock`, `.config/mise/locks/npm-prettier/` and
`uv.lock`. The pipelines keep their jobs, commands and pins. `main` follows through a pull request
on GitHub and a merge request on GitLab. `tasks.md` is the sole progress ledger.
