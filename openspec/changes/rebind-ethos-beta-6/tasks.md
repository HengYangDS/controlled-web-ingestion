# Tasks

## 1. Runtime and declaration

- [x] 1.1 Bind the repository family to the 0.2.0-beta.6 runtime, installed with native Mise from the release's own declaration and checked against its manifest's source commit, through its console's `hook install`, keeping 0.2.0-beta.5 as the rollback; done when CURRENT names the 0.2.0-beta.6 runtime and ROLLBACK the 0.2.0-beta.5 one. Native Mise installed the runtime from the release's declaration; its manifest names 0.2.0-beta.6, source `727ee0579ba1`, digest `0ca012761d1c`. CURRENT names `0ca012761d1c` and ROLLBACK `a4492b26ceca` (0.2.0-beta.5).
- [x] 1.2 Remove the two retired command fields from `.ethos/release.toml` with `ethos lane repair-paradigm --apply`; done when `ethos status` reports the lane ready under the 0.2.0-beta.6 runtime with no retired-field gap. The repair removed both command fields and the emptied `[publication]` header; both peers remain declared. `status` passes with no gap; the lane is dirty only with this Change's edits.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
