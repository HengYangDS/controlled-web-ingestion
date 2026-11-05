# Design

## Context

`uv.lock` resolves dateparser 1.4.3 for `htmldate` 1.11.0, which requires `dateparser>=1.4.3` and
reaches the repository through `trafilatura`. dateparser 1.5.0 is a minor release with breaking
changes. It stops caching `Settings` instances and removes `Settings.registry_key`,
`Locale.to_parserinfo()`, `HijriDate.weekday()` and the fastText leftovers of `dateparser_cli`. It
also changes the `DateData.period` values under `RETURN_TIME_AS_PERIOD`, and deprecates helpers
with a `FutureWarning`.

## Goals / Non-Goals

**Goals:**

- Take dateparser's security fixes as soon as the release is a day old.

**Non-Goals:**

- Changing jobs, commands, the Python matrix, runner selection, the workload set or an image.

## Decisions

### Only the lock moves, by the native release-age option

`uv lock --upgrade --exclude-newer` admits only releases published before the cutoff, and a plain
`uv lock` afterwards drops the persisted `[options] exclude-newer` while keeping every version, so
`uv lock --check` still passes.

### The breaking changes do not reach the only caller

`htmldate` builds one `DateDataParser` with `NORMALIZE`, `PARSERS`, `PREFER_DATES_FROM`,
`PREFER_LOCALE_DATE_ORDER`, `RETURN_AS_TIMEZONE_AWARE` and `STRICT_PARSING`. It reads only
`date_obj` from `get_date_data()`, and it lists month names through
`dateparser.languages.loader.default_loader`. None of the removed or changed names is among these,
and `RETURN_TIME_AS_PERIOD` stays off. No module of this repository imports dateparser.

## Risks / Trade-offs

- [A behavior change alters a date that `htmldate` extracts] → The tests and the hosted matrix run on
  the refreshed lock before landing, and the lock returns to 1.4.3 if either fails.
