# Tasks

## 1. Records

- [x] 1.1 Rename the three archived Change roots to their logical identifiers
  and update the two claim pointers; done when no archive root fails the
  identifier grammar.
- [x] 1.2 Remove both `capability.toml` files and update the contract test;
  done when each capability root holds only `spec.md`.
- [x] 1.3 Rename the decision records to `dr-0001` through `dr-0004` and update
  every reference; done when no reference names an old decision file.
- [x] 1.4 Move the five M1–M5 records to `evidence/benchmarks/` unchanged and
  update the migration map; done when their manifest digests still match.
- [x] 1.5 Add the two chronicle READMEs and remove the empty decision
  groupings; done when every documentation directory has a real entrance.

## 2. Verification

- [x] 2.1 Run strict OpenSpec validation and the repository test, static,
  schema, documentation and security gates; done when all pass.
- [x] 2.2 Run the ETHOS repository audit on a scratch clone of this tree; done
  when it reports no gap.
