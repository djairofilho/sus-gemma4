# Update Specs Prompt

Use this prompt when implementation changes behavior, architecture, validation, data shape, or workflows.

Steps:

1. Identify which spec is stale.
2. Update only the relevant section.
3. Add or update an ADR for architecture changes.
4. Update `specs/plan.md` status if milestone progress changed.
5. Update `tasks/active.md` or `tasks/done.md` if execution state changed.
6. Run `bash scripts/validate.sh` when applicable.

Rules:

- Do not rewrite specs wholesale.
- Keep specs factual and current.
- Prefer durable decisions over chat-history assumptions.
