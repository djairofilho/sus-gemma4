# Security Skill

## Purpose

Use this playbook for privacy, local-first constraints, medical safety, and dependency risk.

## Practices

- Treat clinical text as sensitive even when identifiers are absent.
- Avoid persistence by default.
- Minimize logs and redact inputs where possible.
- Keep local-first behavior explicit and auditable.
- Use official sources for protocol grounding.
- Maintain conservative medical guidance.

## Anti-Patterns

- Sending case text to hosted APIs without explicit architecture approval.
- Committing `.env`, keys, downloaded private data, or real patient examples.
- Producing definitive diagnosis or controlled medication instructions.
- Adding background telemetry.
- Hiding limitations from users.

## Checklist

- [ ] No secrets committed.
- [ ] No real patient identifiers committed.
- [ ] No hidden network calls.
- [ ] Safety notice remains visible.
- [ ] Red flags escalate appropriately.
