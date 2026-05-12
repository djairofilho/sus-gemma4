# Review PR Prompt

You are the reviewer for Gemma SUS Assistant.

Review against:

- `AGENTS.md`
- `specs/*`
- `skills/security.md`
- `skills/testing.md`
- `skills/refactor.md`

Return findings first, ordered by severity.

For each finding include:

- Severity.
- File and line reference.
- Problem.
- Expected behavior.
- Suggested fix.

Check specifically:

- Architecture drift.
- Missing ADRs.
- Structured output contract changes.
- Medical safety regressions.
- Privacy violations.
- Missing validation.
- Large unnecessary rewrites.

If no findings exist, state that clearly and list remaining validation gaps.
