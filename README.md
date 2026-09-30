# MiniPay, Implementation and L2 Support Assessment

This repository implements a small payment processing system with a FastAPI REST service, browser UI, PostgreSQL schema and seed generator, Python L2 support utility, API tests, Playwright UI tests, Kubernetes manifests, and incident investigations.

## Main components

`app/` contains the API and ORM models. `ui/` contains the browser UI. `database/` and `sql/` contain schema, synthetic data generation, operational queries, reconciliation, and performance evidence. `support_tool.py` is the L2 diagnostic CLI. `kubernetes/` contains deployable cluster configuration. `investigation/` contains incident root cause analyses.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. In local direct mode, click Login without entering an API key. For API key mode, set `AUTH_MODE=api_key` and provide `MINIPAY_API_KEY` through the environment, never in source control.

## Docker Compose

```bash
docker compose up --build
```

The UI is available on port 8080 and the API on port 8000. PostgreSQL data is stored in the `pgdata` named volume.

## Tests

```bash
pytest -q tests/api
pytest -q tests/ui
pytest -q
```

The UI suite needs a Playwright browser. Install one with `playwright install chromium`.

## Docker

The API and UI Dockerfiles are in `kubernetes/`. Build with:

```bash
docker build -f kubernetes/Dockerfile.api -t minipay-api:1.0.0 .
docker build -f kubernetes/Dockerfile.ui -t minipay-ui:1.0.0 .
```

## Kubernetes

For a local Kind cluster, build the images and load them before applying the stack:

```bash
docker build -f kubernetes/Dockerfile.api -t minipay-api:1.0.0 .
docker build -f kubernetes/Dockerfile.ui -t minipay-ui:1.0.0 .
kind load docker-image minipay-api:1.0.0
kind load docker-image minipay-ui:1.0.0
```

Create a real Secret from your environment and apply the Kustomize stack:

```bash
kubectl create namespace minipay --dry-run=client -o yaml | kubectl apply -f -
kubectl -n minipay create secret generic minipay-secret --from-literal=DB_PASSWORD="$DB_PASSWORD" --from-literal=DATABASE_URL="postgresql+psycopg://minipay:${DB_PASSWORD}@minipay-db:5432/minipay" --from-literal=MINIPAY_API_KEY="$MINIPAY_API_KEY" --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -k kubernetes/
kubectl -n minipay rollout status deploy/minipay-api
```

Replace the example secret manifest in the rendered environment with real secret material. Never commit it.

## Support utility

```bash
python support_tool.py --transaction TXN00000001
python support_tool.py --transaction TXN00000001 --json
```

## Coverage

See `REQUIREMENTS_MATRIX.md` for a direct mapping from each assessment requirement to the implementation and evidence.

## Git

The work should be reviewed through incremental commits. Branch naming used for the implementation is `main` with focused commits for implementation, tests, infrastructure, and incident documentation. The final submission tag is `submission-v1.0`.


## Direct local login

The local UI uses direct login by default. The Login button does not call an authentication API and does not ask for an API key. Set `AUTH_MODE=api_key` to require `X-API-Key` authentication for backend routes.
