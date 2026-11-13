# Tasks

## 1. Docstring

- [x] 1.1 Shorten the docstring of `src/web_ingestion/adapters/__init__.py` to one line within 100
      columns; done when the code-analysis gate and every `mise run check` command pass. The
      docstring is 97 characters; at `618d5a2` the code-analysis, behavior and tests gates pass, and
      every `mise run check` command passes, 89 tests included.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and
  OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by
  itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge
  request.
