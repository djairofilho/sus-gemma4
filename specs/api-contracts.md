# API Contracts

## Purpose

This file defines stable contracts for internal APIs and structured model outputs. Update this file before or with any contract change.

## Triage Output Schema Draft

```json
{
  "risk_level": "low | moderate | high | emergency",
  "summary": "string",
  "suggested_action": "string",
  "referral": "UBS | UPA | SAMU | emergency | scheduled_follow_up | administrative_guidance | unknown",
  "red_flags": ["string"],
  "sus_basis": ["string"],
  "limitations": "string",
  "safety_notice": "string"
}
```

## Field Rules

- `risk_level` must be one of the allowed values.
- `referral` must be one of the allowed values.
- `red_flags` must be an array, even when empty.
- `sus_basis` must cite retrieved context when RAG is used.
- `limitations` must state that the output does not replace professional evaluation.
- `safety_notice` must include escalation guidance for worsening or severe symptoms.

## Future Endpoints

Draft endpoint names. Implementation requires ADR if backend framework is not already selected.

- `POST /api/triage`: submit case text and receive structured guidance.
- `POST /api/rag/search`: retrieve local protocol snippets.
- `GET /api/health`: verify app, Ollama, and index status.
