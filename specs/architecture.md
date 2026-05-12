# Architecture Spec

## Current Phase

Repository foundation for spec-driven, agent-first development. Application modules will be introduced incrementally.

## Target Stack

- Web app: Vite + React + TypeScript.
- Local backend: to be decided by ADR before implementation.
- Local model runtime: Ollama.
- Base model: Gemma 4 family when available through the selected runtime.
- Fine-tuning: Unsloth with LoRA/QLoRA.
- RAG: local document ingestion, chunking, embeddings, vector search, and cited retrieval.
- Validation: lint, typecheck, tests, build, schema checks, and safety evals.

## Target Modules

- `app/frontend`: user interface, structured result rendering, local UX.
- `app/backend`: local API for model calls, RAG orchestration, schema validation.
- `app/shared`: shared schemas and contracts.
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
