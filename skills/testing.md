# Testing Skill

## Purpose

Use this playbook for unit tests, integration tests, evals, schema regression, and validation loops.

## Practices

- Test pure functions first.
- Use fixtures for structured outputs and eval cases.
- Add regression tests for every safety-sensitive bug.
- Prefer deterministic tests over live model calls.
- Mock Ollama in automated tests unless explicitly running local integration tests.
- Keep eval cases non-identifiable.

## Anti-Patterns

- Removing tests to pass validation.
- Depending on network access for standard validation.
- Using real patient data in fixtures.
- Asserting exact LLM prose when schema properties are the real requirement.

## Checklist

- [ ] Schema-valid output tested.
- [ ] Schema-invalid output rejected.
- [ ] Red-flag escalation covered.
- [ ] Non-emergency administrative routing covered.
- [ ] Validation command updated if tooling changes.
