# Tasks

## 1. Redaction

- [x] 1.1 Redact with
      `ethos lane redact private-addresses --apply --key-stdin --authorize --expect-head <head>`;
      done when a fresh preview reports no occurrence and every `mise run check` command passes. The
      apply at `e9970693` replaced both occurrences on line 84 and updated the sha256 that the claim
      record keeps for the evidence record; the redaction is committed alone as `c72134af`, the
      preview of that head reports no occurrence, and every check command passes, with 89 tests.
- [x] 1.2 Verify with
      `ethos lane redact private-addresses --verify --key-stdin --base <base> --head <head>`; done
      when ETHOS records the `redaction:private-peer` Attestation for the head. The verification of
      `c72134af` from `e9970693` re-derived both occurrences and recorded Attestation `3959d183`.
