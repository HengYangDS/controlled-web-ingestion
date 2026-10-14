## Why

ETHOS releases from c6d6b1e8b on gate prove, land and publish on the common repository paradigm.
This repository's tree has four gaps against its first slice:

- `.ethos/assistants.toml` and `.ethos/project.toml` belong to a superseded binding schema;
- `.ethos/state/.gitignore` tracks a state directory, and tracked state is not admitted;
- `.gitattributes` does not end with the catch-all `* text=auto eol=lf`.

The next paradigm phase also admits only tool-named configuration owners under `.config/`. Its
report already flags `.config/ethos/generated-artifacts.toml`, an adopter copy of the
generated-artifact topology that ETHOS loads from its own package and that nothing here reads.

The repository must switch to such a release to close out its first ETHOS-governed landing, so the
migration and the runtime switch belong to the same batch.

## What Changes

- `.ethos/assistants.toml` is removed. Nothing in the repository or the governing ETHOS release
  reads it.
- `.ethos/project.toml` is removed. Its name duplicates `profile_id` in `.ethos/profile.toml`, and
  the ETHOS boundary contract test now reads the identity from the profile only.
- `.ethos/state/.gitignore` is removed together with its root `.gitignore` exception and its entry
  in the generated-artifact homes. ETHOS keeps its state in the Git common directory and no longer
  writes `.ethos/state`.
- `.config/ethos/generated-artifacts.toml` is removed together with the `.gitignore` comment
  that pointed to it. ETHOS reads its generated-artifact policy from the installed package.
- `.gitattributes` ends with `* text=auto eol=lf`. No tracked file uses CRLF, so nothing is
  renormalized.

## Evidence Boundary

Local evidence only: the repository paradigm report, the repository gates, strict OpenSpec
validation and the ETHOS proof in the Work Lane.

## Non-goals

- Later paradigm slices are not adopted here: common branch-role names, the shared commit grammar
  and tool-named configuration owners follow with the ETHOS releases that enforce them.
