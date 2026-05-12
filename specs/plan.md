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

## Milestone 2: Ollama Integration

- [x] Create model runtime interface.
- [x] Add Ollama client.
- [x] Add local model configuration.
- [x] Add failure states for missing Ollama/model.

## Milestone 3: Structured Outputs

- [~] Define shared JSON schema.
- [~] Validate model output.
- [ ] Add repair or retry strategy.
- [ ] Add schema regression tests.

## Milestone 4: RAG

- [ ] Define document metadata model.
- [ ] Add ingestion pipeline.
- [ ] Add chunking strategy.
- [ ] Add local embeddings/vector search.
- [ ] Add citation rendering.

## Milestone 5: Fine-Tuning Track

- [ ] Define dataset format.
- [ ] Add seed examples.
- [ ] Add Unsloth/QLoRA scripts.
- [ ] Add eval split and safety cases.
- [ ] Document adapter export path.

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
