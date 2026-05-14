# Done

## Repository Foundation

- Created `AGENTS.md` global operating contract.
- Created persistent specs in `specs/`.
- Created OpenCode configuration with planner, implementer, reviewer, and debugger agents.
- Created reusable skills and prompts.
- Created task memory files.
- Created validation and Ralph loop scripts.
- Validated with `bash scripts/validate.sh`.
- Published initial `main` branch.

## Web App Shell

- Added FastAPI/Pydantic backend shell.
- Added `/api/health` endpoint.
- Added mocked `/api/triage` endpoint returning schema-valid structured output.
- Added Vite/React/TypeScript frontend shell.
- Added structured result rendering, loading state, error state, and safety notice.
- Extended validation to cover frontend and backend tooling.
- Opened PR: https://github.com/djairofilho/sus-gemma4/pull/2

## Ollama Integration

- Added opt-in Ollama runtime configuration.
- Added backend model runtime boundary.
- Added Ollama `/api/generate` client with mocked tests.
- Integrated `/api/triage` with live Ollama when `GEMMA_SUS_USE_OLLAMA=true`.
- Added conservative mock fallback for unavailable, invalid, or non-JSON model output.
- Added frontend runtime state rendering.
- Opened PR: https://github.com/djairofilho/sus-gemma4/pull/3

## Structured Output Retry

- Added structured output parser for plain JSON, fenced JSON, and JSON embedded in extra text.
- Added schema regression tests for invalid JSON and invalid enum values.
- Added one correction retry before conservative fallback.
- Documented retry behavior in specs.
- Opened PR: https://github.com/djairofilho/sus-gemma4/pull/4

## SUS Safety Evals

- Added synthetic, non-identifiable safety eval cases.
- Added deterministic eval runner using local mock runtime.
- Added tests for eval loading and property checks.
- Integrated safety evals into `scripts/validate.sh` and CI.
- Opened PR: https://github.com/djairofilho/sus-gemma4/pull/5

## RAG Source Foundation

- Added data source policy for RAG and fine-tuning sources.
- Added official RAG source registry.
- Added fine-tuning and benchmark source registry.
- Added local RAG document layout.
- Added source metadata validator and tests.
- Integrated RAG validation into `scripts/validate.sh`.

## RAG Ingestion Pipeline

- Added local document manifest.
- Added synthetic Portuguese RAG fixture for pipeline tests.
- Added Markdown/text ingestion with section chunking.
- Added local lexical index and search.
- Preserved citation metadata in chunks and search results.
- Integrated ingestion and index build into validation.

## MVP Foundations Completion

- Added backend RAG search API at `POST /api/rag/search`.
- Grounded `/api/triage` with retrieved local RAG context while preserving the triage output schema.
- Extended `/api/health` with RAG index status.
- Added source-backed local RAG seed summaries and improved lexical ranking with accent normalization, stopword filtering, title/section weighting, and phrase boosts.
- Added synthetic fine-tuning JSONL seed, validation, and safety splits.
- Added fine-tuning dataset validation and a non-training Unsloth/QLoRA skeleton.
- Improved demo UX with example cases, backend/runtime/RAG status, citations, and raw JSON rendering.
- Added hackathon demo script in `docs/demo-script.md`.
- Added optional live Ollama eval gate behind `GEMMA_SUS_RUN_LIVE_OLLAMA_EVALS=true`.
- Improved `scripts/validate.sh` so local Bash selects a Python with required validation modules when available.
- Validated and merged PR: https://github.com/djairofilho/sus-gemma4/pull/8

## Official RAG Source Downloads

- Added ignored local raw download area for public official source pages.
- Registered local official page downloads in `data/sources/rag_downloads.yml`.
- Added curated RENAME medicines and BVS MS referral/search overview extracts with manifest provenance.
- Added retrieval and ingestion test coverage for the new official extracts.
- Validated and merged PR: https://github.com/djairofilho/sus-gemma4/pull/12

## Local RAG Retrieval Finalization

- Added sparse local vector embeddings to the generated RAG index.
- Kept deterministic lexical scoring and phrase boosts as fallback signals inside hybrid retrieval.
- Documented hybrid lexical/vector retrieval in RAG specs and README.
- Deferred routine fine-tuning validation behind `GEMMA_SUS_VALIDATE_FINETUNING=true` while RAG release work is prioritized.
