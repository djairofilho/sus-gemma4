# Requirements

## Objectives

- Provide a local-first web assistant for SUS-oriented workflows.
- Use Ollama for local inference with Gemma-family models when available.
- Use RAG for official SUS protocols and public clinical-administrative materials.
- Produce structured outputs suitable for validation and downstream UI rendering.
- Maintain a fine-tuning track from the beginning using curated behavioral datasets.

## Functional Requirements

- Accept Brazilian Portuguese clinical-administrative user input.
- Normalize and preserve common Brazilian healthcare terminology.
- Retrieve relevant protocol context from local indexed documents.
- Generate structured JSON for triage/routing support.
- Generate a plain-language explanation for the user interface.
- Identify red flags and recommend emergency escalation when appropriate.
- Differentiate clinical guidance from administrative routing.
- Support offline/local operation after models and documents are available locally.
- Maintain eval cases for SUS terminology, safety behavior, and schema validity.
- Maintain fine-tuning datasets and scripts separately from runtime RAG.

## Non-Functional Requirements

- Local-first by default.
- Deterministic validation workflows.
- Minimal external dependencies.
- Clear module boundaries.
- Fast onboarding for AI agents.
- Reproducible build and validation commands.
- Structured logs without sensitive patient data.
- Small, reviewable changes.

## Constraints

- Do not store identifiable patient data unless a future ADR defines retention, encryption, and LGPD controls.
- Do not call hosted model APIs by default.
- Do not provide definitive diagnosis.
- Do not prescribe controlled medications.
- Do not replace clinical evaluation.
- Do not encode protocol facts only in fine-tuning when they should come from RAG.

## Out Of Scope For Initial MVP

- Production EHR integration.
- Patient identity management.
- Cloud deployment.
- Full medical diagnosis automation.
- Automated prescription generation.
