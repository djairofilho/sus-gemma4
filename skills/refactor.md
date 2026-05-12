# Refactor Skill

## Purpose

Use this playbook for restructuring code without changing behavior.

## Practices

- Define preserved behavior before changing structure.
- Keep refactors small and reviewable.
- Prefer moving code before changing code.
- Run tests before and after when possible.
- Update imports mechanically and validate.

## Anti-Patterns

- Combining refactor with feature work.
- Rewriting files for style preference.
- Introducing abstractions without reuse or clarity.
- Changing public contracts without updating specs and ADRs.

## Checklist

- [ ] Behavior change is not intended.
- [ ] Tests or validation establish equivalence.
- [ ] Specs updated only if structure affects architecture.
- [ ] Diff is focused.
