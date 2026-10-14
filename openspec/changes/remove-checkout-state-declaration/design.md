## Context

ETHOS retired checkout-local mutable state. Its runtime resolves the state database under the Git
common directory, and its own `.ethos/rules.toml` no longer declares `state_path`. This repository
still declares the retired path, which no producer writes and no reader consumes.

## Decisions

1. Remove the field instead of pointing it at the Git common directory. The runtime owns that
   location, so a declared copy would be a second authority without a consumer.
2. Keep `state_tracked_truth = false`. ETHOS keeps the same field in its own binding.

## Rollback

Revert this change. The rules file again declares a state path that nothing reads.
