# Design

## Context

ETHOS's code-analysis gate runs Ruff with `--line-length 100` and the `E,F,B,I,UP` rules on every
tracked Python file. The repository's own Ruff configuration did not report the 109-character
docstring, so the lane's checks passed and the proof did not.

## Goals / Non-Goals

**Goals:**

- Keep every package docstring on one line within 100 columns.

**Non-Goals:**

- Changing any other docstring, source file or check.

## Decisions

### Drop a word, keep the purpose

"Acquisition adapters: in-memory static extraction and the loopback-only Firecrawl protocol." names
the same two adapters in 97 characters with its quotes.

## Risks / Trade-offs

- [Another line exceeds the gate's limit] → The code-analysis gate runs on the working edit before
  the commit.
