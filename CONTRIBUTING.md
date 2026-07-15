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

Follow [repository conventions](docs/reference/conventions.md) before committing:
semantic units use one blank line, Python module-level definitions use two, and
machine-readable configurations contain no decorative blank lines.
