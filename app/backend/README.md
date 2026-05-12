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

## Configuration

Environment variables use the `GEMMA_SUS_` prefix.

- `GEMMA_SUS_USE_OLLAMA`: enable live Ollama calls when set to `true`.
- `GEMMA_SUS_OLLAMA_BASE_URL`: defaults to `http://localhost:11434`.
- `GEMMA_SUS_OLLAMA_MODEL`: defaults to `gemma3:4b` until the target Gemma 4 runtime is available.
- `GEMMA_SUS_OLLAMA_TIMEOUT_SECONDS`: defaults to `30`.
