## Context

An ETHOS proof compiles the profile's code-correctness map and requires the gate of each axis to
carry a product quality verifier. The verifiers observe the committed Python subjects of the tree.
Behavior runs the locked pytest with JUnit, report-log and coverage output, and requires every
product source file to be measured and exercised. Static analysis runs isolated Ruff with the
product rule set at the shared width of 100, and ShellCheck without a configuration file.

## Decisions

1. Add provider gates instead of rewriting the native gates. The native test, topology, schema,
   documentation and security commands stay repository-owned and keep running. The providers add the
   product evidence that the proof requires.
2. Declare `tools/**` as tooling. Tests load several tooling scripts, so the scripts appear in the
   coverage report. Tooling still receives static analysis, but only product source owes behavior
   coverage.
3. Format at 100 columns. That is the width the product static verifier measures and the width of
   every configured formatter in the governed repositories, so the formatting churn happens once.
4. Keep the runtime script compatible with Bash 3.2. The CLI runs `bash` from `PATH`, which is Bash
   3.2 on a stock macOS. The ShellCheck fix therefore pipes container identifiers to `xargs` instead
   of using `mapfile`.
5. Call the native tools directly. Both CI jobs already declare the wrapper's two uv variables, uv
   creates the cache and environment directories itself, and a proof gate uses uv's default cache
   and environment. The proof gates request no interpreter, so uv selects one under
   `requires-python` and no POSIX-only executable name such as `python3` is needed.
6. Declare both hosted repositories. GitHub's `main` starts at the GitLab-published `main` instead
   of the local release root, which the delivery decision forbids pushing directly. Both planes then
   advance only through reviewed proposals with their own hosted checks.

## Rollback

Revert this change. The proof floor returns to the native gates, and an ETHOS proof blocks again on
the missing verifiers. No runtime, evidence or target is touched.
