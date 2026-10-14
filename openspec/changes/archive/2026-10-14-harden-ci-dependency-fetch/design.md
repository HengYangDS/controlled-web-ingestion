## Context

Each runner of the pair keeps its own `/cache` volume, so a review run never warms the protected
runner's uv cache. A first protected run therefore downloads every wheel over the CI host's
network.

## Decisions

1. Use uv's native network settings rather than a GitLab `retry` on script failure. uv retries
   only the failed request, while a job retry would also repeat a genuine test failure.
2. Lower download concurrency to 8. Fifty parallel downloads share one guest network path, and
   fewer streams finish more large wheels within each timeout.
3. Keep the caches separate. Sharing one cache between the review and protected runners would let
   unprotected code influence protected builds.

## Rollback

Revert this change. uv returns to its defaults, and a transient download failure fails the job
again.
