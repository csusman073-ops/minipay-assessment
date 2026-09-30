# Assessment Coverage Matrix

| Requirement | Implementation / evidence |
|---|---|
| Linux | `evidence/linux.md`, `evidence/linux-runtime.txt`, `scripts/healthcheck.sh` |
| Git | Incremental commit history and final tag `submission-v1.0` |
| SQL | `sql/queries.sql`, `sql/reconciliation.sql`, `sql/PERFORMANCE.md`, `database/schema.sql` |
| 50,000 plus data | `database/generate_data.py`, `evidence/data-generator.txt`, `scripts/benchmark_transaction_search.py` |
| Kubernetes | `kubernetes/namespace.yaml`, `configmap.yaml`, `secret.example.yaml`, `postgres.yaml`, `api.yaml`, `ui.yaml`, `ingress.yaml`, `kustomization.yaml` |
| Starter defect analysis | `investigation/kubernetes-findings.md` |
| Rancher | `evidence/rancher.md`, with environment limitation documented |
| Python L2 tool | `support_tool.py`, `tests/test_support_tool.py` |
| REST API | `app/main.py`, `tests/api/test_api.py` |
| API automation | `tests/api/`, `evidence/api-test.txt` |
| UI automation | `tests/ui/test_ui.py`, `evidence/ui-test.txt`, `evidence/ui-test.png` |
| Incident 001 | `investigation/INCIDENT-001-RCA.md`, reproducible fixture and test |
| Incident 002 | `investigation/INCIDENT-002-RCA.md` |
| Incident 003 | `investigation/INCIDENT-003-RCA.md`, benchmark evidence |
| AI usage | `AI_USAGE.md` |
| Reproducible setup | `SETUP.md`, `docker-compose.yml`, Dockerfiles, CI workflow |
