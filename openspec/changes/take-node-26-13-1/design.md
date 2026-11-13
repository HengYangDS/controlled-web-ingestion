# Design

## Context

`.config/mise/config.toml` declares the local tools, and `.config/mise/mise.lock` pins each one's
archive and checksum per platform. Node runs the declared Prettier in `mise run check`. The hosted
pipelines install their tools without Mise, so this lock reaches only local checks.

## Goals / Non-Goals

**Goals:**

- Run the local checks on Node 26.13.1, the security release of the declared line.

**Non-Goals:**

- Moving any other tool. Prettier 3.10.1, uv 0.13.8 and Ruff 0.17.5 become a day old later and move
  in the next supply lane.
- Changing a pipeline, a job, a command or a pin.

## Decisions

### Only node moves, through the native lock

The configuration names the new release, and `mise lock` writes its archives and checksums for every
locked platform. The lane refuses the result unless node's entries are the only ones that change and
the lockfile version holds.

## Risks / Trade-offs

- [A check depends on Node 26.13.0] → Every `mise run check` command runs on 26.13.1 before the
  commit; restoring the previous declaration and lock rolls it back.
