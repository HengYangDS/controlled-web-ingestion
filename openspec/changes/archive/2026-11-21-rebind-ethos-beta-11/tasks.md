# Tasks

## 1. Runtime

- [x] 1.1 Bind the repository family to the 0.2.0-beta.11 runtime, installed with native Mise from
      the release's own declaration and checked against its manifest's source commit, through its
      console's `hook install`, keeping 0.2.0-beta.10 as the rollback; done when CURRENT names the
      0.2.0-beta.11 runtime and ROLLBACK the 0.2.0-beta.10 one, and `ethos status` reports the lane
      ready. The release read back with every platform published; native Mise installed its runtime
      from the release's own declaration, whose manifest names source commit e4d9d04d3; the
      console's `hook install` passed. CURRENT names the 0.2.0-beta.11 runtime `8c663b10…` and
      ROLLBACK the 0.2.0-beta.10 runtime `526c2eba…`; `ethos status` reports the lane ready, and the
      paradigm repair preview reports the tree conforming.
- [x] 1.2 Name 0.2.0-beta.11 as the pin floor in the README's frozen status; done when the
      documentation gates pass. The README's status names ETHOS 0.2.0-beta.11; the format check and
      the documentation gates pass.

## 2. Release age

- [x] 2.1 Change `minimum_release_age` from "0h" to "24h" under `[settings]` in
      `.config/mise/config.toml`; done when `mise settings get minimum_release_age` prints `24h` in
      the lane and `mise install --locked` installs the locked tools unchanged. Read in the lane:
      `24h`; `mise install --locked` exits 0 with every tool already installed.
- [x] 2.2 Declare uv's release age, `exclude-newer = "24 hours"` under `[tool.uv]` in
      `pyproject.toml`, and relock in the same commit with `uv lock`; done when `git diff uv.lock`
      changes no `[[package]]` entry (the lock's header records `exclude-newer-span = "PT24H"`) and
      `uv lock --check` and `uv sync --frozen` pass. If the relock would move a package, stop: the
      repository is frozen. The relock changes only the lock's `[options]` header
      (`exclude-newer-span = "PT24H"`) and no `[[package]]` entry; `uv lock --check` and
      `uv sync --frozen` exit 0.

## Workflow follow-up

- Archive this Change and prove the archived head once.
- Publish the proposal, wait for both forges' review jobs, land, publish `dev` and `main`, and read
  the protected jobs back; then retire the lane.
