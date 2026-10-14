## ADDED Requirements

### Requirement: GitLab CI runs only on the declared project runner pair

The repository SHALL run GitLab CI only on its project-locked docker-executor runner pair on the
dedicated CI host. Ref protection SHALL select the runner, and every job SHALL name a
digest-pinned image. Any other runner, including one in a person's login session, is a personal
runner.

#### Scenario: a protected ref pipeline runs

- **WHEN** a pipeline runs for a protected ref
- **THEN** its jobs carry the `ci-linux-arm64-container-protected` tag
- **AND** only the project's protected runner can take them

#### Scenario: a review pipeline runs

- **WHEN** a pipeline runs for an unprotected ref or a merge request
- **THEN** its jobs carry the `ci-linux-arm64-container` tag

#### Scenario: a job starts

- **WHEN** a GitLab job starts
- **THEN** its image is a digest reference
- **AND** the job runs without privileged mode or the host Docker socket
