## Context

The CI Linux ARM64 host is a dedicated Parallels guest, isolated from the host OS, and already runs
the GitLab runner pairs of the owner's other governed projects. Each pair carries two tags:
`ci-linux-arm64-container` for review pipelines and `ci-linux-arm64-container-protected` for
protected refs. GitLab only gives protected-ref jobs to the protected runner.

## Decisions

1. Adopt the existing pair pattern instead of a project-specific layout. Workflow rules set
   `WIB_CI_RUNNER_TAG` from `CI_COMMIT_REF_PROTECTED`, and every job uses that tag.
2. Use explicit jobs per Python version, each with its own digest-pinned uv image, rather than a
   matrix. Each job then names exactly one image, and the runner allowlist can list it.
3. Use the full trixie variants. `tools/ci/check_documentation.py` reads `git ls-files`, and only
   the full images ship git.
4. Keep uv offline about interpreters (`UV_PYTHON_DOWNLOADS=never`) so the image's Python is the
   tested Python. The uv cache lives on the runner's `/cache` volume.
5. Scan the full history in the security job with `GIT_DEPTH: "0"`, as GitHub does with
   `fetch-depth: 0`. The gitleaks image's entrypoint is cleared so that GitLab runs the job script.
6. Amend DR-0003 instead of working around it. The runner contract becomes explicit, and the
   personal-runner prohibition keeps its meaning.

## Risks

- The CI host is part of the owner's workstation. When it is down, the GitLab plane is blocked;
  DR-0003 records such an outage as an external block.
- The first job on each runner pulls its image, and later jobs reuse it.

## Rollback

Revert this change and re-enable runner 129. The shell projection returns unchanged.
