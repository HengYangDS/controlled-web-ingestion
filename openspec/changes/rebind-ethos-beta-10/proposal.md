## Why

The repository runs ETHOS 0.2.0-beta.9 through the family's runtime selection; it tracks no ETHOS
version. The owner asked that every governed repository run the latest ETHOS release.

The owner also approved a frozen state for a repository without a named consumer, and this
repository is its first: after this move it takes no further ETHOS bind or supply Change until a
named consumer appears or a security advisory needs one.

Its adopter-facing changes since 0.2.0-beta.9 are these:

- **Breaking: Markdown lists follow one blank-line rule** in the Markdown format, its check, the
  Markdown gate and `pre-commit`: a list item with one paragraph is followed directly by the next
  item. A file that breaks it fails `markdown_list_spacing:<path>:<line>` until
  `ethos lane format --apply` repairs it in a Work Lane.
- **Breaking: the canonical text files have an acting owner.** INI and `.cfg` files, the Vale
  vocabularies, `LICENSE`, `VERSION`, `.editorconfig`, `.gitattributes`, `.gitignore`, `.gitkeep`,
  `.shellcheckrc` and the CI supply's `Dockerfile` and `.dockerignore` take no blank line at the
  start or the end, at most one in a row and one final newline; the source-format gate reports
  `source_format_drift:<path>`.
- **Breaking: every authored `__init__.py` opens with a docstring** that names its package's
  purpose, or the paradigm reports `repository_paradigm_package_docstring:<path>`.
- **Breaking: every README that the docs registry admits declares `role: index`** and holds at most
  100 lines that are not blank; docs health reports `docs_readme_not_index:<path>` and
  `docs_index_too_long:<path>:<lines>>100`.
- A paradigm refusal that `ethos lane repair-paradigm` can repair names its preview as the next
  action, and `.config/mise/mise.lock` is required only when `.config/mise/config.toml` selects a
  tool.
- Its Node.js supply moves to 26.13.1, a security release with nine High-severity fixes under seven
  CVE identifiers.
- It upgrades directly from 0.2.0-beta.9 and keeps result schema 3. A rollback after the declaration
  repair is not qualified. Among its known open defects, npm 12.2.2 still bundles `glob` 13.0.6 and
  `minimatch` 10.2.5 (GHSA-3g3m-2fjr-6pw4, GHSA-g3hv-75wg-m249), and Go's GO-2026-6859 still affects
  the bundled `cue`, `vale` and `shfmt`, which ETHOS runs only as local commands over repository
  files without starting an HTTP server.

## What Changes

- Bind the repository family to the 0.2.0-beta.10 runtime, installed with native Mise from the
  release's own declaration, through its console's `hook install`, keeping 0.2.0-beta.9 as the
  rollback.
- Repair the list spacing that 0.2.0-beta.10's Markdown list rule refuses in the July implementation
  plan: 13 blank lines go and no words. The Markdown gate checks that file, but
  `ethos lane format --apply` leaves it alone because this repository's Prettier ignore names
  `docs/plans/`, so the lane applies the rule with the bound runtime's own `canonical_spacing`.
- State in the README that the repository is frozen after this move: its pin floor, ETHOS
  0.2.0-beta.10 with the supply of 14 November 2026, and its thaw condition, a named consumer or a
  security advisory.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion policy, its tests and its publication behave as before, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The repository-common runtime selection,
`docs/plans/2026-07-14-controlled-web-ingestion-topology-implementation.md` (blank lines only) and
`README.md`. `tasks.md` is the sole progress ledger.
