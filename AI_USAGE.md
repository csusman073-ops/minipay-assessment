# AI Usage

AI assistance was used to accelerate repository scaffolding, test case design, documentation structure, and review of Kubernetes and SQL patterns.

Representative interactions:

1. Asked for a production minded FastAPI layout with PostgreSQL, health checks, validation, authentication, and idempotent payment creation.
2. Asked for API test cases covering 4xx, 5xx, authentication, idempotency, schema assertions, and response time.
3. Asked for a Kubernetes review of the supplied broken Deployment and Service, specifically focusing on selectors, ports, probes, resources, and secrets.
4. Asked for SQL queries for daily status summaries, top customers, stale processing records, duplicates, success rates, reconciliation, and p95 processing time.
5. Asked for an L2 support CLI design with concise human output, JSON mode, logging, timeouts, and exit codes.

Validation approach: generated code was executed through Python compilation, pytest, API tests, and static YAML inspection. Database queries were reviewed against PostgreSQL syntax. Kubernetes manifests were reviewed for selector and port consistency.

Material correction example: an initial generated support utility omitted URL encoding for transaction references and did not distinguish numeric IDs from references cleanly. The implementation was corrected to use `urllib.parse.quote` for search values and separate numeric ID lookup from reference lookup. The Kubernetes design was also adjusted so probes and Service target ports consistently use the actual API listener on 8000.


## Validation and ownership

AI suggestions were treated as drafts rather than as authoritative implementation. I checked generated code by running the test suite, compiling Python modules, exercising the API through the test client, executing the browser journey with Playwright, validating Kubernetes YAML structurally, reviewing SQL against the supplied schema, and reproducing the documented Incident 001 defect. I also corrected issues discovered during validation, including route matching order, SQLite identifier behavior, direct login behavior, and proxy path handling.

I can explain the final code and modify it without relying on the AI session.
