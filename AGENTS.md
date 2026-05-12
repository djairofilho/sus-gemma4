# AGENTS.md

Global operating contract for AI agents working on Gemma SUS Assistant.

## Project Identity

Gemma SUS Assistant is a local-first web application for Brazilian public healthcare workflows. It adapts Gemma 4 usage patterns to Brazilian Portuguese clinical-administrative contexts, SUS protocols, structured outputs, Ollama-based local inference, RAG over official public documents, and a fine-tuning track with Unsloth/QLoRA.

This project is not a diagnostic automation product. Agents must preserve the positioning as a protocol-aware assistant for triage support, administrative routing, documentation, and safety-oriented guidance.

## Mandatory Workflow

Every non-trivial change must follow this sequence:

1. Read the relevant specs in `specs/`.
2. Check `tasks/active.md` and `tasks/backlog.md`.
3. Produce or update an incremental plan in `specs/plan.md` or `tasks/active.md`.
4. Implement the smallest correct change.
5. Run `scripts/validate.sh` or the closest available validation command.
6. Review the diff against requirements, architecture, security, and validation specs.
7. Update docs/specs/tasks when behavior, architecture, or workflow changes.

Skipping specs is a process violation.

## Required Reading Before Coding

Agents must read these files before implementing features:

- `specs/product.md`
- `specs/requirements.md`
- `specs/architecture.md`
- `specs/validation.md`
- `specs/plan.md`

Agents must also read relevant skills from `skills/`:

- Frontend work: `skills/frontend.md`
- Backend work: `skills/backend.md`
- RAG work: `skills/rag.md`
- Fine-tuning work: `skills/ml-finetuning.md`
- Security-sensitive work: `skills/security.md`
- Test work: `skills/testing.md`
- Refactors: `skills/refactor.md`
- Agent workflow work: `skills/agents.md`

## Architecture Control

Do not introduce architectural changes without an ADR in `specs/decisions/`.

Architectural changes include:

- Changing the runtime, framework, persistence layer, model server, or inference strategy.
- Introducing new service boundaries.
- Changing public API contracts.
- Changing structured output schemas.
- Changing privacy, safety, or medical-risk behavior.
- Adding external hosted dependencies to a local-first workflow.

Use ADR filenames like `0002-use-fastapi-for-local-backend.md`.

## Editing Rules

- Prefer minimal diffs.
- Preserve existing behavior unless the spec requires a change.
- Do not rewrite files wholesale when targeted edits are sufficient.
- Keep names explicit and domain-relevant.
- Do not add backward compatibility unless there is a concrete persisted or external contract.
- Do not add hidden network calls in local-first workflows.
- Do not add medical claims that exceed the product scope.
- Do not store sensitive patient data unless a spec explicitly defines the storage model and retention policy.

## Medical Safety Rules

The assistant must:

- Avoid definitive diagnosis.
- Avoid prescribing controlled medications.
- Encourage emergency care for red flags.
- State limitations clearly.
- Prefer SUS pathways: UBS, UPA, SAMU, emergency, regulation, follow-up.
- Use RAG evidence when protocol-specific guidance is requested.
- Preserve Brazilian Portuguese clinical-administrative terminology.

## Definition Of Done

A change is done only when:

- Requirements are satisfied.
- Structured output contracts remain valid.
- `scripts/validate.sh` passes or unavailable validation is explicitly documented.
- Specs or tasks are updated when necessary.
- Security and medical safety risks are considered.
- The diff is small and reviewable.

## Documentation Sync

Update specs when the change alters:

- Product behavior: `specs/product.md` or `specs/requirements.md`.
- Architecture: `specs/architecture.md` plus an ADR.
- APIs or schemas: `specs/api-contracts.md`.
- Data shape or retention: `specs/data-model.md`.
- Validation: `specs/validation.md`.
- Roadmap or status: `specs/plan.md` and `tasks/*`.

## Multi-Agent Protocol

- Planner owns decomposition and spec alignment.
- Implementer owns small code changes and local validation.
- Reviewer owns risk, regression, security, and spec drift checks.
- Debugger owns failing validation loops and root-cause analysis.

Agents should hand off with concrete file references, current status, failed commands, and remaining risks.

## Commit Convention

Use Conventional Commits:

- `feat(scope): add capability`
- `fix(scope): correct behavior`
- `docs(scope): update documentation`
- `chore(scope): maintain repository tooling`
- `refactor(scope): restructure without behavior change`
- `test(scope): add or update tests`
- `build(scope): update build tooling`
- `ci(scope): update automation`
