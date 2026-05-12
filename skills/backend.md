# Backend Skill

## Purpose

Use this playbook for local API, Ollama integration, schema validation, RAG orchestration, and backend boundaries.

## Practices

- Keep model access behind a small runtime interface.
- Validate inputs and outputs at API boundaries.
- Return structured errors with actionable messages.
- Avoid logging sensitive case details.
- Keep RAG retrieval separate from generation.
- Make local/offline behavior explicit.

## Anti-Patterns

- Calling hosted services by default.
- Mixing prompt construction with HTTP routing.
- Accepting unvalidated model JSON.
- Storing raw patient inputs without a data retention spec.
- Hardcoding protocol guidance outside RAG/evals/specs.

## Checklist

- [ ] Contract documented in `specs/api-contracts.md`.
- [ ] Input validation exists.
- [ ] Output schema validation exists.
- [ ] Ollama failure mode is handled.
- [ ] Tests cover success and failure paths.
