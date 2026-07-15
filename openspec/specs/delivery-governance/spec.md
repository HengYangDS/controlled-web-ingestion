# Delivery Governance

## Purpose

Delivery governance keeps Controlled Web Ingestion publication reproducible,
evidence-bound, and independent of any unreviewed local execution path.

## Requirements

### Requirement: Delivery governance preserves controlled authority

The repository SHALL preserve its policy, evidence, and protected-publication
boundaries when it changes a hosted delivery projection.

#### Scenario: a hosted delivery change is proposed

- **WHEN** a change introduces or modifies a hosted delivery projection
- **THEN** it identifies the affected repository authority, verification command,
  protection boundary, and evidence limitation
- **AND** it does not widen ingestion targets, data classes, runtime topology,
  persistent storage, or integration surfaces by implication

### Requirement: Delivery projections preserve reviewable text layout

The repository SHALL define a single cross-format text-layout convention for
reviewed source, documentation, and configuration. The convention SHALL use
one blank line between adjacent semantic units, reserve two blank lines for
Python module-level definitions, and prohibit decorative blank lines in JSON
and JSONL.

#### Scenario: tracked documentation or configuration is verified

- **WHEN** repository-owned documentation verification runs
- **THEN** it rejects missing final newlines, trailing whitespace, three or
  more consecutive blank lines, and blank lines in JSON or JSONL
- **AND** it does not mutate serialized evidence or runtime outputs
