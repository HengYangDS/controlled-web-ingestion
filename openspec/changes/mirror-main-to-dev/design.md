# Design

## Context

ETHOS reads the release mirror from `.ethos/release.toml`. Without a declaration it is
`independent`: closeout advances `dev` only, and `main` moves only through a release. With
`accepted_ff`, closeout advances `dev` and `main` together, and `main` must stay a fast-forward of
`dev`. ETHOS admits a closeout against the incumbent policy of `dev`, so the closeout that lands
this Change still runs as `independent`; a second closeout then finds `main` behind `dev` and
fast-forwards it. `main` at `afc677c` is an ancestor of `dev`.

DR-0003 requires a GitHub pull request with GitHub Actions and a GitLab merge request with GitLab CI
before each platform's protected `main` moves. On 14 October 2026 pull requests 1 to 4 and merge
requests 3 to 6 were opened, their checks passed, and `main` was then pushed to the reviewed head,
so each records a merge commit equal to its head. GitHub's ruleset on `main` requires a pull
request and the checks `Python 3.12`, `Python 3.13`, `Python 3.14` and `Security`, and lets the
owner bypass it. GitLab lets Maintainers push to the protected `main` and runs no merge-request
pipelines here, so a merge request's evidence is the branch pipeline of the same commit.

## Goals / Non-Goals

**Goals:**

- Keep `main` a fast-forward of `dev` after every landing, on both forges.
- Keep each platform's own review path before its `main` moves.

**Non-Goals:**

- Cutting a release, changing the version, adding a tag, or changing the tag pattern.
- Changing workflows, pipelines, rulesets, branch protection or runners.

## Decisions

### `main` mirrors `dev` through the native release mirror

`accepted_ff` makes ETHOS advance both protected refs in one admitted transaction, so `main` never
diverges from `dev` and no hand-made ref move is needed. An independent release would leave `main`
stale until a first version is chosen, which the owner did not want.

### Each publication of `main` keeps its pull request and merge request

After `dev` is published to both forges, a pull request on GitHub and a merge request on GitLab,
each from `dev` to `main`, carry the head's hosted checks. When both pass, the fast-forward of
`main` is published to both forges, and each forge records its request as merged because `main`
then contains the request's head. Publishing the identical signed commit to GitHub uses the owner's
existing ruleset bypass, because a GitHub merge would rewrite the commits.

## Risks / Trade-offs

- [The landing that introduces the mirror leaves `main` behind] → The second closeout aligns it, as
  ETHOS directs a misaligned mirror to accepted closeout.
- [A publication of `main` waits for two more hosted runs] → It adds about 15 to 20 minutes to a
  landing, and `dev` publishes without waiting.
- [The bypass could also skip checks] → `main` is published only after the pull request's and the
  merge request's checks pass on the exact head.

## Migration Plan

Land this Change, run closeout again so `main` reaches `dev`, publish `dev`, open the pull request
and the merge request, and publish `main` when their checks pass. To roll back, remove the `mirror`
line; `main` stays where it is and moves only through a release again.
