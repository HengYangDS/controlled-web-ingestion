# Tasks

## 1. Version identity

- [x] 1.1 Add `VERSION` (`0.1.0`) and read the package version from it in `pyproject.toml`; done when `uv lock --check` passes, the built package reports 0.1.0 and the paradigm report shows no version-source gap. `VERSION` holds `0.1.0`; `pyproject.toml` declares `dynamic = ["version"]` and reads it through `[tool.hatch.version]`; a plain `uv lock` dropped only the project's own static version line, `uv lock --check` passes, and the installed project reports 0.1.0.
- [x] 1.2 Add the MIT `LICENSE`; done when the paradigm report shows no license gap. `LICENSE` carries the MIT License with the same copyright holder as the other governed repositories.
- [x] 1.3 Rewrite `CHANGELOG.md` to Keep a Changelog 1.1.0 with an `[Unreleased]` section; done when the paradigm report shows no changelog-heading gap. `CHANGELOG.md` follows Keep a Changelog 1.1.0 with a bracketed `[Unreleased]` section that summarizes what 0.1.0 will release.
- [x] 1.4 Declare `[protected_refs] tags = ["v*"]` in `.ethos/release.toml` and drop the unread `version_source` and `tag_pattern` keys; done when the paradigm report shows no release-tags gap and every `mise run check` command passes. `.ethos/release.toml` declares `[protected_refs] tags = ["v*"]` and keeps only `mirror` under `[release]`; every `mise run check` command passes, 89 tests included, with no leaks found.
