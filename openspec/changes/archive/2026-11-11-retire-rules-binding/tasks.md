# Tasks

## 1. Record roots

- [x] 1.1 Run `ethos lane repair-paradigm --apply` until its preview reports `conforming`; done when
      `.ethos/profile.toml` declares `record_roots = ["evidence/"]`, `.ethos/rules.toml` is gone
      with its four tables, the governance-closeout specification names the binding file set
      that remains, and the keyless redaction preview reports both occurrences inside the
      effective record roots. Two apply runs: the first wrote `record_roots = ["evidence/"]` and
      removed `[command_plane]`, `[formats]` and `[gates]`; the second removed `[artifacts]` and
      the file. The preview then reported `conforming`, and the keyless redaction preview
      found 2 occurrences, both inside the roots.
- [x] 1.2 Give `.config/checks/taplo/taplo.toml` the shipped `[formatting]` and `[schema]` settings
      of ETHOS 0.2.0-beta.7, keeping its file selection; done when `ethos lane format --check`
      passes and Taplo reports no other file to reformat. The format check first refused
      `native_formatter_policy_conflict:.ethos/profile.toml`; with the shipped settings, format
      apply opened the repaired array at two-space indentation, every lane check passed, and
      Taplo's own check reports 0 unformatted files.
