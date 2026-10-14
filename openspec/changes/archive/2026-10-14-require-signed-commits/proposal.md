## Why

ETHOS publishes only a source commit whose SSH signature verifies against the host trust anchor.
It signs the commits that it creates, such as Change archives, only when the repository declares
a commit policy that requires signatures. This repository declares none, so every archive head is
unsigned and `ethos publish` rejects it. ETHOS declares the same policy in its own
`.ethos/workspace.toml`.

## What Changes

- `.ethos/workspace.toml` gains a `[commit_policy]` table with the ETHOS subject grammar,
  `signing_required = true` and `signing_format = "ssh"`.
- New commits, including ETHOS archive commits, carry SSH signatures and grammar-conforming
  subjects. Existing history is unchanged.

## Evidence Boundary

Local evidence only: strict OpenSpec validation, the repository gates, the ETHOS proof in the Work
Lane and native signature verification of the new commits.

## Non-goals

- Existing commits are not re-signed. Evidence records name their current IDs, and publication
  verifies only the published head.
- The hosted pipelines do not run ETHOS, so they need no trust anchor.
