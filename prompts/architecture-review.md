# Architecture Review Prompt

You are performing an architecture review for Gemma SUS Assistant.

Review:

- Runtime choices.
- Module boundaries.
- Local-first guarantees.
- RAG and fine-tuning separation.
- Structured output contracts.
- Privacy and medical safety constraints.
- Validation strategy.

Output:

- Findings ordered by severity.
- ADRs required.
- Spec updates required.
- Recommended smallest next decision.

Rules:

- Do not approve hidden hosted dependencies.
- Do not approve persistence of sensitive data without retention policy.
- Do not approve architecture changes without ADR.
