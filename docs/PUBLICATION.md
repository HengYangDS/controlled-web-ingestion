# Publication Boundary

This repository is a sanitized, versioned publication of the Web-Ingestion
admission experiment. It intentionally contains only source code, policy,
tests, portable documentation, and body-redacted evidence.

It intentionally excludes the original local sandbox, runtime secrets,
Open WebUI state, credentials, mutable logs, project virtual environments, and
raw `results/` output. The local sandbox must not be initialized or published
as a whole.

Evidence files under `evidence/benchmarks/` are snapshots. Re-running a
benchmark or changing images, Compose topology, targets, data flow, or routing
requires new evidence and a new admission decision; historical evidence is not
silently overwritten.
