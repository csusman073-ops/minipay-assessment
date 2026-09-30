[SETUP.md](https://github.com/user-attachments/files/32855577/SETUP.md)
# Setup

## Local API

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AUTH_MODE=direct
export DATABASE_URL='sqlite:///./minipay.db'
python -m app.seed
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Docker Compose

```bash
docker compose up --build
```

This starts PostgreSQL, the API, and the UI with health checks.

## PostgreSQL

Set:

```bash
export DATABASE_URL='postgresql+psycopg://minipay:REPLACE@127.0.0.1:5432/minipay'
```

Then apply `database/schema.sql` and load generated data from `database/generate_data.py`.

## Browser tests

```bash
playwright install chromium
pytest -q tests/ui
```

## Kubernetes

See `kubernetes/` and `evidence/rancher.md`. The cluster should have an ingress controller for the `minipay.local` host or you can port forward the UI Service.

## Configuration

`DATABASE_URL`, `AUTH_MODE`, `MINIPAY_API_KEY`, `MINIPAY_API_URL`, and `MINIPAY_TIMEOUT` are environment driven. No secrets are hard coded in deployment configuration. The committed `.env.example` contains placeholders only.

## Git submission

The repository uses incremental Git commits and the final version is tagged `submission-v1.0`. Add your GitHub remote and push the branch and tag:

```bash
git remote add origin <YOUR_PUBLIC_REPOSITORY_URL>
git push -u origin main
git push origin submission-v1.0
```

## Direct local login

For local assessment use, the app defaults to `AUTH_MODE=direct`. The browser Login button is a direct local UI action and does not call an authentication API or ask for an API key.

To restore API key authentication, set `AUTH_MODE=api_key` and provide `MINIPAY_API_KEY` before starting Uvicorn.
