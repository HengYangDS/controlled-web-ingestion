## ADDED Requirements

### Requirement: Branch roles are declared completely

The repository SHALL declare every field of the ETHOS branch-role table, so that ETHOS admits ref
movement with the repository's own roles instead of product defaults.

#### Scenario: ETHOS lands a Work Lane

- **WHEN** ETHOS moves the candidate train to a proven Work Lane head
- **THEN** it reads the repository's complete branch-role table
- **AND** it classifies the candidate branch by its declared role
