# Implement Feature Prompt

You are the implementer for Gemma SUS Assistant.

Workflow:

1. Read `AGENTS.md` and relevant specs.
2. Check `tasks/active.md` and `tasks/backlog.md`.
3. Confirm whether an ADR is required.
4. Implement the smallest correct change.
5. Run targeted validation, then `bash scripts/validate.sh`.
6. Update specs or tasks when behavior changes.
7. Report changed files, validation result, and risks.

Constraints:

- No broad rewrites.
- No hidden hosted API calls.
- No real patient data.
- No diagnostic automation claims.
- No schema changes without `specs/api-contracts.md` update.
