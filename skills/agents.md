# Agent Workflow Skill

## Purpose

Use this playbook when coordinating planner, implementer, reviewer, debugger, or external agent loops.

## Practices

- Start from specs, not assumptions.
- Keep one active objective per agent handoff.
- Prefer file references and command outputs over summaries.
- Treat `tasks/active.md` as execution state and `specs/` as durable memory.
- Hand off with current status, changed files, validation result, and known risks.

## Anti-Patterns

- Coding before reading specs.
- Letting multiple agents edit the same files without coordination.
- Using vague tasks such as "improve app".
- Treating chat history as the only memory.
- Skipping validation because the change is small.

## Checklist

- [ ] Relevant specs read.
- [ ] Active task identified.
- [ ] Minimal implementation scope defined.
- [ ] Validation command selected.
- [ ] Handoff includes files, status, and risks.
