# Architecture

MiniPay has three layers.

The UI is a small browser application served from nginx in Kubernetes. It calls the REST API with an API key header.

The API is FastAPI running on port 8000. SQLAlchemy provides typed models and parameterized queries. Health checks validate database connectivity. Payment creation uses an idempotency key to make client retries safe.

PostgreSQL is the durable data store. Customers, transactions, and callback attempts are separate tables with foreign keys. Selective indexes support transaction investigation, customer payment history, status based operations, and callback lookup. The database runs as a StatefulSet with a persistent volume claim.

The Kubernetes layer separates configuration from secret material and uses readiness and liveness probes plus resource controls. Rolling updates keep service available during normal deployments.
