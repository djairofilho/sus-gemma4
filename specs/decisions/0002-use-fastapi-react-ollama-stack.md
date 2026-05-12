# ADR 0002: Use FastAPI, React, and Ollama Stack

## Status

Accepted

## Context

Gemma SUS Assistant needs a local-first web application that can integrate with Ollama, validate structured outputs, support RAG over official SUS documents, and maintain a fine-tuning track from the beginning. The project also needs fast iteration for a hackathon while preserving clear boundaries for safety, privacy, and future ML workflows.

## Decision

Use the following application stack:

- Frontend: Vite + React + TypeScript.
- Backend: Python + FastAPI + Pydantic.
- Local model runtime: Ollama.
- RAG, evals, and fine-tuning support: Python-first modules and scripts.
- Structured output validation: Pydantic in the backend, with frontend TypeScript types kept in sync through shared schema documentation or generated types when tooling is introduced.

## Rationale

- FastAPI and Pydantic are a strong fit for schema validation, local API boundaries, and ML/RAG workflows.
- Python keeps RAG, evals, embeddings, and Unsloth/QLoRA fine-tuning close to the backend ecosystem.
- Vite + React + TypeScript keeps the web UI fast, lightweight, and suitable for structured output rendering.
- Ollama preserves the local-first inference requirement and avoids hosted model calls by default.

## Consequences

- The repository will include both Python and Node/TypeScript tooling.
- `scripts/validate.sh` must eventually run both backend and frontend validation commands.
- Schemas must avoid drifting between Pydantic and TypeScript representations.
- Live Ollama calls should be mocked in default automated tests unless explicitly running local integration tests.
- Future changes to backend framework, frontend framework, or model runtime require a new ADR.

## Alternatives Considered

- Node/Fastify + Zod for a single TypeScript stack. Rejected because Python better supports the planned RAG, eval, and fine-tuning workflow.
- Python-only web UI. Rejected because React provides a stronger interactive demo surface for structured output rendering.
- Hosted model API. Rejected because local-first/offline operation is a core requirement.
