# Proposal

## Why

GitLab `main` pipeline 14240 failed on 5 November 2026 in one job, Python 3.14. In
`test_scrape_uses_loopback_api_and_returns_only_needed_result_fields`, the first recorded request
was `/v1/crawl/crawl-1` instead of `/v1/scrape`. The same tests passed on `dev` and on GitHub, and
the retried job passed. The Firecrawl fixture server in `tests/unit/test_firecrawl_client.py` is
shared by the whole test class, and its handler threads record every request into one class-level
list. The crawl-timeout test lets its client give up after 0.01 seconds, so a handler thread for
one of its requests can still run after the next test has cleared the list, and it then records
its stale path in that test. Under host load the race shows; a test must not depend on thread
timing.

## What Changes

- Give every Firecrawl client test its own fixture server, and keep the recorded requests and the
  simulated crawl status on that server instead of on the handler class.
- Close each server after its test so that `server_close()` waits for every handler thread, and
  treat a client that disconnects on purpose as the expected end of its request instead of
  printing a traceback.
- Let the crawl-timeout test read its log only after its own requests have finished, and give its
  client 0.2 seconds with 0.02-second polls instead of 0.01 and 0.001, so that the crawl request
  itself cannot time out under load.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Only a unit-test fixture changes. Ingestion behavior and its contracts do not, so
`.openspec.yaml` sets `skip_specs: true`.

## Impact

`tests/unit/test_firecrawl_client.py` only. The four tests keep their names and assertions, and the
suite keeps 89 tests. `main` follows through a pull request on GitHub and a merge request on
GitLab. `tasks.md` is the sole progress ledger.
