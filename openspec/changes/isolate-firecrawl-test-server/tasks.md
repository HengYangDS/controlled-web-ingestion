# Tasks

## 1. Test fixture

- [x] 1.1 Give each Firecrawl client test its own fixture server that records only its own requests and whose close waits for its handler threads; done when a forced late handler thread no longer reaches the next test and every `mise run check` command passes. On the old fixture, a harness that held the crawl-timeout test's first poll until the next test's `setUp` reproduced job 65601's failure (`'/v1/crawl/crawl-1' != '/v1/scrape'`), and one that delayed its poll and cancel handlers by 0.3 s failed the timeout test itself (`'/v1/crawl' != '/v1/crawl/crawl-1'`). With one server per test both pass, 30 repeated runs of the module pass, and all nine `mise run check` commands pass, including 89 tests.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge request.
