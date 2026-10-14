## Why

The paradigm migration removed every `.ethos/state` exception it found, but `.ethos/rules.toml`
still declares `state_path = ".ethos/state/state.sqlite"` in its `[artifacts]` table. ETHOS keeps
its state database in the Git common directory, no ETHOS reader of the field remains, and ETHOS
removed the same line from its own binding. The accepted `governance-closeout` requirement already
forbids a tracked declaration of a state directory under `.ethos/`, so the line is a conformance
gap.

## What Changes

- `state_path` is removed from the `[artifacts]` table of `.ethos/rules.toml`.
- The binding requirement names the rules file, so the declaration cannot return unnoticed.

## Evidence Boundary

Local evidence only: strict OpenSpec validation, the repository gates and the ETHOS proof in the
Work Lane.

## Non-goals

- Untracked files that older runtimes left in checkouts are host state, not repository content,
  and stay outside this change.
