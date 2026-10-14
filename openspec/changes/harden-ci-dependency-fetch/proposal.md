## Why

The first runs on the new GitLab runner pair failed twice while fetching wheels from
`files.pythonhosted.org`: once on a 126-second timeout and once on a DNS lookup error. The same
commit passed on the review runner, and both failed jobs passed when re-run. uv's defaults (3
retries, a 30-second request timeout, 50 concurrent downloads) suit a fast network, not the CI
host's shared path.

## What Changes

- The GitLab Python jobs set `UV_HTTP_RETRIES=10`, `UV_HTTP_TIMEOUT=120` and
  `UV_CONCURRENT_DOWNLOADS=8`, so uv itself absorbs transient download failures.
- The runner requirement states that a transient dependency download is retried inside the job
  and that a test failure is never retried.

## Evidence Boundary

Local: strict OpenSpec validation, the repository gates and the ETHOS proof. Hosted: the next
GitLab pipelines on both runners.

## Non-goals

- No job-level retry of script failures, which would also retry real test failures.
- No change to GitHub Actions, whose hosted network has not failed.
