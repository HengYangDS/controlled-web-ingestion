# Design

## Context

`.config/mise/config.toml` declares the local tools, and `.config/mise/mise.lock` pins each one's
archive and checksum per platform. Ruff and Prettier run in `mise run check`, and uv resolves
`uv.lock`. The hosted jobs install their tools without Mise: GitHub's from the pipeline model's
pins, GitLab's inside uv images that the model pins by digest.

## Goals / Non-Goals

**Goals:**

- State the release age where the tool that applies it reads it.
- Run the local checks on the latest stable Ruff and Prettier, and resolve against the latest stable
  packages.

**Non-Goals:**

- Moving uv to 0.13.8. It moves together with the three GitLab job images, which the shared runners
  must first admit and load.
- Retiring the repository's own format gates in favor of ETHOS's shipped ones; that is a Change of
  its own.

## Decisions

### The age is one line of Mise configuration

Mise applies a release age to every tool it resolves and reads it from `minimum_release_age`. The
repository uses no other update proposer, so that line is the age's only tracked home; the uv lock
takes its cutoff from the same value when it is refreshed.

### Each tool moves through the native lock

The configuration names each release, and `mise lock` writes its archives and checksums for every
locked platform. The lane refuses the result unless only the moved tools' entries change and the
lockfile version holds.

### The uv lock keeps no cutoff

`uv lock --upgrade --exclude-newer` takes the releases up to the declared age, and a plain `uv lock`
afterwards keeps the cutoff out of the lock file.

## Risks / Trade-offs

- [A release a few hours old is broken or withdrawn] → The lock pins every hash, OSV is read for the
  moved lock, and every `mise run check` command and the full proof run before landing; restoring
  the previous declarations and locks rolls it back.
- [Prettier 3.10 and ETHOS's 3.9.10 disagree on a later edit] → Both accept today's tree; a later
  disagreement fails one of the two checks before a commit.
- [uv stays one patch release behind] → 0.13.8 carries no security note; a security release of uv
  would justify the runner change at once.
