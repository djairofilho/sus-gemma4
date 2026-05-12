# ADR 0001: Agent-First Spec-Driven Repository

## Status

Accepted

## Context

The project will be developed with AI agents and human collaborators. Without persistent specs, agents can drift, duplicate decisions, introduce architecture changes silently, or skip validation.

## Decision

Use a spec-driven repository structure with:

- `AGENTS.md` as the global operating contract.
- `specs/` as persistent project memory.
- `skills/` as specialized playbooks.
- `prompts/` as reusable agent instructions.
- `tasks/` as lightweight execution state.
- `scripts/validate.sh` as the standard validation entrypoint.
- `scripts/ralph.sh` as the iterative validation loop entrypoint.

## Consequences

- Agents must read specs before coding.
- Architecture changes require ADRs.
- Validation becomes a required part of the workflow.
- Documentation must evolve with behavior.
- Initial repository overhead is higher, but drift risk is lower.
