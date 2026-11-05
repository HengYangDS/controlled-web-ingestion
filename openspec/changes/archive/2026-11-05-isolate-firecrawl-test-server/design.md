# Design

## Context

`FirecrawlClientTests` starts one `ThreadingHTTPServer` in `setUpClass`. Its handler records each
request in the class attribute `_FirecrawlHandler.requests`, and `setUp` clears that list. The
standard library serves each request in its own thread. `ThreadingHTTPServer` makes those threads
daemons, and `server_close()` waits only for threads that are not daemons. In
`test_crawl_timeout_cancels_the_remote_job` the client polls with a 0.01-second budget, so it can
give up on a request before the server thread has handled it. That thread then records
`/v1/crawl/crawl-1` whenever it is scheduled, which can be after the next test has cleared the
list. The trace of job 65601 in pipeline 14240 shows exactly that: two `BrokenPipeError`
tracebacks from handler threads whose client had gone, then the scrape test's first recorded path
`/v1/crawl/crawl-1`.

The same test reads the log as soon as its client gives up, so under load its own poll and cancel
requests can still be unrecorded at that moment. With a 0.01-second budget even its crawl request
can time out before the job exists.

## Goals / Non-Goals

**Goals:**

- Make each Firecrawl client test observe only its own requests, whatever the thread timing.

**Non-Goals:**

- Changing the client, its timeouts, the tests' assertions or any other test module.

## Decisions

### One server per test, closed together with its handler threads

A small `ThreadingHTTPServer` subclass owns the recorded requests and the simulated crawl status.
It sets `daemon_threads = False`, so `server_close()` joins every handler thread. It also treats
`BrokenPipeError` and `ConnectionResetError` as the expected end of a request whose client gave up.
`setUp` starts one server per test and registers its shutdown and close as cleanups. A late handler
thread can then record only into its own test's server, and it finishes before the next test
starts.

### The crawl-timeout test waits for its own requests

The test closes its server, which joins the handler threads, before it reads the log, and gives its
client 0.2 seconds with 0.02-second polls. The simulated crawl never completes, so the client still
times out on a poll and cancels the job, and the assertion is unchanged.

## Risks / Trade-offs

- [A handler thread that never ends would block `server_close()`] → No handler waits on anything:
  each one answers at once or fails on the closed socket, and the serving thread is joined with a
  5-second limit.
