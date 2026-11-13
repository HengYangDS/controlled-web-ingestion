# Design

## Context

ETHOS's docs registry admits the Markdown under `docs/` and checks each page's front matter. Its
0.2.0-beta.10 rule reserves a directory's `README.md` for navigation: the README declares
`role: index` and stays within 100 nonblank lines, and other content lives on named pages. Its
repository paradigm also asks every tracked `__init__.py` to open with a docstring. Both are
report-only gaps.

## Goals / Non-Goals

**Goals:**

- Every README under `docs/` declares `role: index`.
- Every package marker opens with a one-line docstring naming its purpose.

**Non-Goals:**

- Rewriting any page's content, or changing any contract, test or tool.
- Binding ETHOS 0.2.0-beta.10, which happens in its own Change after its release.

## Decisions

### The owner's split decides each README

ETHOS's owner decided on 13 November 2026: the evidence and history READMEs are already indexes in
content (a scope table with links, and a scope sentence with links), so only their role changes. The
start README is a first-run guide, so its body moves unchanged to `first-run.md` as a how-to page,
and the directory keeps a short index README because it then holds two pages.

### Docstrings state purpose, not contents

Each docstring is one sentence naming what the package is for, from its modules and callers, so it
stays true as files change.

## Risks / Trade-offs

- [A link still points at the start guide's old path] → The root README's link moves to
  `first-run.md`; the docs index keeps linking the directory's README, which now routes to the
  guide; the documentation check resolves every local link.
