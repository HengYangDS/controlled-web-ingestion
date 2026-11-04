# Tasks

## 1. Release mirror

- [x] 1.1 Declare `mirror = "accepted_ff"` under `[release]` in `.ethos/release.toml`; done when the ETHOS configuration, format and paradigm checks pass on the lane. The ETHOS format, configuration, OpenSpec and status checks and the repository's TOML format gate pass on the lane.

## 2. Decisions

- [x] 2.1 Record in DR-0002 and DR-0003 that `main` mirrors `dev` and keeps each platform's reviewed change path; done when the documentation, Markdown and prose checks pass. The docs registry, the repository's documentation and document-format gates, and the Markdown, Markdown-link and prose checks pass.

## Workflow follow-up

- Archive this Change and prove the archived head; publish it as a proposal to GitLab and GitHub, and wait for both hosted runs.
- Land and close out, then run closeout again so `main` fast-forwards to `dev`; publish `dev`, open a pull request and a merge request from `dev` to `main`, publish `main` when their checks pass, and retire the proposal refs and the lane.
