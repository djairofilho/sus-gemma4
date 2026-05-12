# Demo Script

## Goal

Show Gemma SUS Assistant as a local-first SUS workflow assistant, not a diagnostic automation product.

## Setup

1. Start backend: `cd app/backend && uvicorn app.main:app --reload --port 8000`.
2. Start frontend: `cd app/frontend && npm run dev`.
3. Optional Ollama: set `GEMMA_SUS_USE_OLLAMA=true` and confirm the local model is available.
4. Build RAG index if needed: `python -m rag.scripts.search_index --build`.

## Talk Track

1. Open the web app and point out local backend, runtime, and RAG status.
2. Submit the urgent UBS example: `Paciente relata PA 18x12, cefaleia forte e falta de ar. Esta na UBS.`
3. Explain the structured output: risk level, referral, red flags, cited SUS basis, limitations, and safety notice.
4. Open the JSON panel to show downstream-friendly schema output.
5. Submit the administrative example and show that it routes to administrative/UBS guidance without inventing diagnosis.
6. Submit the controlled prescription example and show refusal/safety boundaries.

## Safety Positioning

- The app supports acolhimento, routing, documentation, and safety-oriented guidance.
- It does not diagnose, prescribe controlled medication, or replace professional evaluation.
- Protocol-specific details should come from local RAG documents with citations.

## Validation Summary

Before demo, run `bash scripts/validate.sh`. If Bash resolves a Python without installed tools, run the backend, RAG, safety, and fine-tuning Python checks with the local Windows Python.
