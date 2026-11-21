# Tasks

## 1. Runtime

- [ ] 1.1 Bind the repository family to the 0.2.0-beta.11 runtime, installed with native Mise from
      the release's own declaration and checked against its manifest's source commit, through its
      console's `hook install`, keeping 0.2.0-beta.10 as the rollback; done when CURRENT names the
      0.2.0-beta.11 runtime and ROLLBACK the 0.2.0-beta.10 one, and `ethos status` reports the lane
      ready.
- [ ] 1.2 Name 0.2.0-beta.11 as the pin floor in the README's frozen status; done when the
      documentation gates pass.

## 2. Release age

- [ ] 2.1 Change `minimum_release_age` from "0h" to "24h" under `[settings]` in
      `.config/mise/config.toml`; done when `mise settings get minimum_release_age` prints `24h`
      in the lane and `mise install --locked` installs the locked tools unchanged.
- [ ] 2.2 Declare uv's release age, `exclude-newer = "24 hours"` under `[tool.uv]` in
      `pyproject.toml`, and relock in the same commit with `uv lock`; done when
      `git diff uv.lock` changes no `[[package]]` entry (the lock's header records
      `exclude-newer-span = "PT24H"`) and `uv lock --check` and `uv sync --frozen` pass.
      If the relock would move a package, stop: the repository is frozen.

## Workflow follow-up

- Archive this Change and prove the archived head once.
- Publish the proposal, wait for both forges' review jobs, land, publish `dev` and `main`, and read
  the protected jobs back; then retire the lane.
