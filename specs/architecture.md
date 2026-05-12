# Architecture Spec

## Current Phase

Repository foundation is complete. The next phase is the initial web application shell using the accepted FastAPI, React, and Ollama stack.

## Target Stack

- Frontend: Vite + React + TypeScript.
- Local backend: Python + FastAPI + Pydantic.
- Local model runtime: Ollama.
- Base model: Gemma 4 family when available through the selected runtime.
- Fine-tuning: Unsloth with LoRA/QLoRA.
- RAG: local document ingestion, chunking, embeddings, vector search, and cited retrieval.
- Validation: lint, typecheck, tests, build, schema checks, and safety evals.

See `specs/decisions/0002-use-fastapi-react-ollama-stack.md` for the accepted stack decision.

## Target Modules

- `app/frontend`: user interface, structured result rendering, local UX.
- `app/backend`: local API for model calls, RAG orchestration, schema validation.
- `app/shared`: shared schema documentation, generated types, or contract fixtures.
- `rag`: ingestion, chunking, embeddings, retrieval, document metadata.
- `finetuning`: datasets, training scripts, notebooks, adapters, eval exports.
- `evals`: regression and safety cases.
- `docs`: supporting product, demo, and methodology materials.

## Core Flow

1. User submits a Brazilian Portuguese case.
2. Backend validates input and strips unnecessary identifiers.
3. RAG retrieves relevant official SUS context.
4. Prompt builder combines system policy, user case, retrieved context, and JSON schema.
5. Ollama runs local inference.
6. Backend validates structured output.
7. UI renders risk level, pathway, red flags, cited basis, and safety notice.

## Separation Of Responsibilities

Fine-tuning teaches:

- Brazilian Portuguese clinical style.
- SUS workflow behavior.
- Structured output discipline.
- Refusal and safety behavior.
- Terminology normalization.

RAG provides:

- Protocol details.
- Updated official guidance.
- Source citations.
- Local document grounding.

## Architecture Rules

- Keep model runtime replaceable behind a small interface.
- Keep RAG retrieval separate from generation.
- Keep schemas shared and validated at boundaries.
- Keep fine-tuning artifacts out of application runtime paths.
- Use ADRs for stack and boundary decisions.
- Keep default tests deterministic by mocking live Ollama calls.
