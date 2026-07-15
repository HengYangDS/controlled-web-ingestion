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
