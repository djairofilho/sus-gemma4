# Incremental Plan

## Status Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete

## Milestone 0: Repository Foundation

- [x] Create agent operating contract.
- [x] Create persistent specs.
- [x] Create OpenCode configuration.
- [x] Create skills and prompts.
- [x] Create validation and Ralph loop scripts.

## Milestone 1: Web App Shell

- [x] Select application stack via ADR.
- [x] Create local web app shell.
- [x] Add structured result components.
- [x] Add responsive demo layout.
- [x] Add demo examples, local status, citations, and raw JSON panel.

## Milestone 2: Ollama Integration

- [x] Create model runtime interface.
- [x] Add Ollama client.
- [x] Add local model configuration.
- [x] Add failure states for missing Ollama/model.

## Milestone 3: Structured Outputs

- [x] Define shared JSON schema.
- [x] Validate model output.
- [x] Add repair or retry strategy.
- [x] Add schema regression tests.

## Milestone 4: RAG

- [x] Define document metadata model.
- [x] Add ingestion pipeline.
- [x] Add chunking strategy.
- [x] Add local embeddings/vector search.
- [x] Add citation rendering.

## Milestone 5: Fine-Tuning Track

- [x] Define dataset format.
- [x] Add seed examples.
- [x] Add Unsloth/QLoRA scripts.
- [x] Add eval split and safety cases.
- [x] Document adapter export path.

## Milestone 6: Review And Release Discipline

- [~] Establish branch naming.
- [~] Establish PR template.
- [~] Add CI once app tooling exists.
- [~] Require validation and review before merge.

## Branch And PR Policy

- `main` is the stable integration branch.
- Use short-lived branches with Conventional Commit-aligned prefixes: `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`, `test/`, `build/`, `ci/`, `style/`.
- Open PRs for non-trivial changes.
- Each PR must state specs read, validation run, safety/privacy impact, and architecture/API/schema impact.
- Merge only after validation passes and review risks are resolved.

## Current Risks

- Gemma 4 runtime availability in Ollama may require model-specific adjustment.
- Protocol document licensing and provenance must be tracked.
- Medical safety expectations must remain conservative.
- Fine-tuning data quality can create unsafe behavior if not evaluated.
- Ollama is opt-in and falls back to conservative mock output if unavailable or invalid.
- Structured output parser accepts plain JSON, fenced JSON, and JSON embedded in extra text.
- SUS safety evals currently run against deterministic mock triage output; live-model evals remain future work.
- Optional live Ollama evals are implemented behind `GEMMA_SUS_RUN_LIVE_OLLAMA_EVALS=true`; deterministic mock evals remain the default.
- RAG source registries are defined and validated before document ingestion.
- RAG currently supports local Markdown/text ingestion, source-backed seed summaries, hybrid lexical/vector search with Portuguese normalization/ranking improvements, sparse local embeddings, and cited retrieval.
- Fine-tuning currently has synthetic JSONL seed, validation, and safety splits plus dataset validation and a non-training QLoRA skeleton; real training and routine validation are deferred until RAG release work is complete.
- Demo UX now shows backend/runtime/RAG status, example cases, cited basis, and raw structured JSON for hackathon review.
- Official document acquisition is manual-first: commit small curated Markdown/text extracts with provenance, keep large downloads local/ignored, and validate manifest metadata before indexing.
- Public fine-tuning datasets should be downloaded only for local review first; committed examples remain synthetic until license and privacy policy changes are explicitly defined.
