# Backend

Local FastAPI backend for Gemma SUS Assistant.

## Development

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /api/health`: verifies local API status.
- `POST /api/triage`: returns a schema-valid mocked triage response for the web app shell.

The current shell does not call Ollama. Live model integration will be added in a separate feature.
