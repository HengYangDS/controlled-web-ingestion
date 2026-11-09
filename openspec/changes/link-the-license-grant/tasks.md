# Tasks

## 1. License entry

- [x] 1.1 Link `LICENSE` from a License section of `README.md` and declare `license = "MIT"` with `license-files = ["LICENSE"]` in `pyproject.toml`; done when the proof preview reports no `license-entry` gap, `uv lock --check` passes and every `mise run check` command passes. `README.md` ends with a License section that links `LICENSE`, and `pyproject.toml` declares `license = "MIT"` with `license-files = ["LICENSE"]`; the installed project reports License-Expression MIT, `uv lock --check` passes and every `mise run check` command passes, 89 tests included.
