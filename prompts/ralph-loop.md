# Ralph Loop Prompt

You are running an iterative Ralph-style development loop for Gemma SUS Assistant.

Loop contract:

1. Read specs and active task.
2. Select one small change.
3. Implement only that change.
4. Run validation.
5. If validation fails, fix only the root cause.
6. Repeat until validation passes or the iteration limit is reached.
7. Stop and report status.

Stopping conditions:

- Validation passes.
- Maximum iterations reached.
- Architecture decision is required.
- Safety or privacy risk is unclear.
- The task requires human input.

Each iteration report must include:

- Iteration number.
- Files changed.
- Validation command and result.
- Next action or stopping reason.
