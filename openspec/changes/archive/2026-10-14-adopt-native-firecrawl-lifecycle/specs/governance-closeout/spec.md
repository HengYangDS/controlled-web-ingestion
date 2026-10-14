## ADDED Requirements

### Requirement: The Firecrawl runtime runs under native Compose and the product lifecycle

The repository SHALL declare the complete Firecrawl topology in its Compose projection with digest
references and healthchecks, and SHALL start, use and remove that topology only through
`web-ingest`, without a repository shell controller.

#### Scenario: a browser request runs the disposable topology

- **WHEN** an admitted browser or crawl request reaches the Firecrawl route
- **THEN** `web-ingest` verifies the reviewed image identities before startup
- **AND** it starts the topology with `docker compose up --wait` and publishes only
  `127.0.0.1:13002`
- **AND** it removes the project with its volumes and verifies that no project resource remains

#### Scenario: a run fails after startup

- **WHEN** the staged request fails while the topology is running
- **THEN** `web-ingest` still removes the project and verifies zero remaining resources
- **AND** the request reports the failure

#### Scenario: the authorized workload set is validated

- **WHEN** an operator runs `web-ingest validate-workloads --evidence PATH`
- **THEN** the reviewed static, browser and crawl workloads, the duplicate, promotion and bridge
  steps, and the service loopback-scrape rejection are checked
- **AND** one body-redacted evidence record is written only after every check passes
