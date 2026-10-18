# Contributing

Use the ETHOS command plane for local repository changes:

```bash
ethos status
ethos plan --changed
ethos prove
ethos land
ethos publish
ethos report
```

Mutating operations such as `ethos land` and `ethos publish` require explicit
authorization and expected HEAD binding.

`mise run bootstrap` installs the locked tools and Python environment from
`.config/mise/`; `mise run check` runs every repository check, and `mise run fix`
regenerates the Forge pipelines from `.config/ci/pipeline.cue` and applies the
formatters.

Follow [repository conventions](docs/reference/conventions.md) before committing:
semantic units use one blank line, Python module-level definitions use two, and
machine-readable configurations contain no decorative blank lines.
