# Tasks

## 1. Runtime

- [x] 1.1 Bind the repository family to the 0.2.0-beta.8 runtime, installed with native Mise from
      the release's own declaration and checked against its manifest's source commit, through its
      console's `hook install`, keeping 0.2.0-beta.7 as the rollback; done when CURRENT names the
      0.2.0-beta.8 runtime and ROLLBACK the 0.2.0-beta.7 one, and `ethos status` reports the lane
      ready. The release read back with all five platforms; the installed runtime's manifest names
      source commit `9bf5bdda7`; the manifests of `CURRENT` and `ROLLBACK` name 0.2.0-beta.8 and
      0.2.0-beta.7; the paradigm repair reports `conforming`; status after the bind passes, dirty
      only by this Change's documents.
