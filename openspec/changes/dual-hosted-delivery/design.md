# Design

## Equal hosted planes

GitHub and GitLab each retain repository truth and a thin CI projection over
`tools/ci/`. They are not active-active runtime services and neither platform
synchronizes or publishes the other automatically. Candidate parity is an
explicit release condition: the same reviewed candidate commit must be observed
at each remote before separate protected-main publications.

## GitHub Actions projection

The GitHub workflow uses Ubuntu hosted runners, a Python 3.12/3.13/3.14 matrix,
least-privilege read-only repository permission, and reviewed commit pins for
third-party actions. It invokes owner commands instead of duplicating tests or
shell checks. The action-native Gitleaks scan remains its detector; a temporary
shim lets the repository security-command contract run without pretending that
the shim performed the scan.

## Failure and rollback

A missing GitHub repository, unavailable GitLab, missing eligible runner,
failed hosted job, candidate divergence, or absent branch protection blocks
only the corresponding publication step. No fallback may weaken a gate or
create a personal standing runner. Reverting this change removes the GitHub
projection and decision material; it does not require runtime teardown.
