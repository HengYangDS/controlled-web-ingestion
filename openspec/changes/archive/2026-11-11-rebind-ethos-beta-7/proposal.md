## Why

The repository runs ETHOS 0.2.0-beta.6 through the family's runtime selection; it tracks no ETHOS
version. The owner asked that every governed repository run the latest ETHOS release.

Its adopter-facing changes since 0.2.0-beta.6 are these:

- **The root commands select one declared catalog operation.** A request whose flags select no
  operation, or that sets a flag its operation does not take, exits 2 with
  `command_operation_unmatched:<command>` or `command_field_refused:<field>`; a preview refuses
  `--authorize`; negated flags such as `--no-apply` are gone; usage errors exit 2 with a
  `usage_refused` result. One prose sentence of the July topology design names `adopt --dry-run`, as
  a record of that time; no command path uses it.
- `next.form` names the catalog operation, whose effects, destructiveness and authorization `next`
  carries.
- `ethos lane repair-paradigm` moves a `rules.toml` `[artifacts]` table into the profile's
  `record_roots`, and deletes the `rules.toml` tables that no reader consults; this repository's
  `[command_plane]`, `[formats]` and `[gates]` go in `redact-peer-addresses`, after this Change.
- Under `required`, push admission refuses a peer feed that the clone cannot know, and the redaction
  verb answers `unknown` without a known feed.
- Every governed repository keeps `VERSION` and a Keep a Changelog `CHANGELOG.md`, and `[release]`
  admits only `mirror`. This repository already conforms since `establish-version-identity`.
- `ethos --version` names the source commit again.
- `ethos lane prewrite --target index --patch <file>` checks an exact selective staging patch against
  the index instead of the working file, reusing staged admission; the worktree target stays the
  default. Nothing in this repository depends on it.
- **Breaking (exit status and publication):** a usage error exits 2 with `usage_refused`, an
  undeliverable result exits 3, `ethos publish --ref … --probe-remote` exits 1 when its verdict is
  `unknown`, and `ethos publish --apply` takes only a probe's `--receipt`. This repository's tracked
  files and CI call none of these forms, and the npm launcher that beta.7 removes was never used
  here.
- `pre-commit` refuses a staged file of a registered language above the paradigm's per-file code
  ceiling, which the proof already enforced.
- An exception from one proof gate or one of its providers now refuses only that gate, as
  `gate_runner_error:<gate>` or `gate_provider_error:<gate>:<provider>`, while every other gate
  keeps running and keeps its evidence; a timeout stays `unknown`.

## What Changes

- Bind the repository family to the 0.2.0-beta.7 runtime, installed with native Mise from the
  release's own declaration, through its console's `hook install`, keeping 0.2.0-beta.6 as the
  rollback.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The ingestion policy, its tests and its publication behave as before, so `.openspec.yaml` sets
`skip_specs: true`.

## Impact

The repository-common runtime selection only. `tasks.md` is the sole progress ledger.
