# Gemma SUS Assistant

Local-first web assistant for Brazilian public healthcare workflows using Gemma 4, Ollama, RAG over official SUS materials, structured outputs, and a fine-tuning track with Unsloth/QLoRA.

## Positioning

This project is not a medical diagnosis replacement and does not compete with general medical models as a broad diagnostic system. It focuses on Brazilian Portuguese clinical-administrative workflows, SUS pathways, protocol-aware guidance, and low-infrastructure/offline operation.

## Repository Workflow

This repository is optimized for spec-driven and agent-first development.

Start here:

- `AGENTS.md`
- `specs/product.md`
- `specs/requirements.md`
- `specs/architecture.md`
- `specs/validation.md`
- `specs/plan.md`

Run validation:

```bash
bash scripts/validate.sh
```

## Local App Shell

Backend:

```bash
cd app/backend
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd app/frontend
npm install
npm run dev
```

Run an iterative Ralph-style loop:

```bash
bash scripts/ralph.sh
```
