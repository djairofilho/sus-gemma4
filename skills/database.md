# Database Skill

## Purpose

Use this playbook if persistence is introduced for indexes, metadata, evals, or future user data.

## Practices

- Add an ADR before introducing a persistence layer.
- Keep patient data out of scope unless data retention is specified.
- Separate public document metadata from user-submitted content.
- Make migrations reproducible.
- Use explicit retention and deletion rules for sensitive data.

## Anti-Patterns

- Adding a database because it is convenient.
- Persisting raw case text without a privacy model.
- Mixing vector index metadata with application user records.
- Creating irreversible migrations without review.

## Checklist

- [ ] ADR exists.
- [ ] Data model updated.
- [ ] Retention policy documented.
- [ ] Migration path tested.
- [ ] Sensitive data handling reviewed.
