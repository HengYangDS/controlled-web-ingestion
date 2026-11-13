# Tasks

## 1. Documentation indexes

- [x] 1.1 Declare `role: index` in `docs/evidence/README.md` and `docs/history/README.md`; done when
      the documentation check passes. Both declare `role: index` with 24 and 14 nonblank lines, and
      `check_documentation.py` passes.
- [x] 1.2 Move the start guide's body to `docs/start/first-run.md`, make `docs/start/README.md` its
      directory's index, and point the root README's link at the guide; done when every
      `mise run check` command passes. `first-run.md` keeps the guide's subject, role, relations and
      body; the new index has 12 nonblank lines and links both pages; every `mise run check` command
      passes, 89 tests included.

## 2. Package docstrings

- [x] 2.1 Open each of the six empty `__init__.py` files with a one-line docstring that names the
      package's purpose; done when every tracked package marker opens with a docstring and every
      `mise run check` command passes. All tracked `__init__.py` files open with a docstring
      (`ast.get_docstring`, the rule's own test), and every `mise run check` command passes.

## Workflow follow-up

- Resulting-HEAD proof, integration, official archive and exact lane retirement are native ETHOS and
  OpenSpec records.
- Hosted acceptance follows publication: the published `dev` push starts the GitHub workflow by
  itself, and it and the GitLab pipeline pass. `main` follows through one pull request and one merge
  request.
