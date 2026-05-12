# Product Spec

## Name

Gemma SUS Assistant

## Vision

Build a local-first clinical-administrative assistant adapted to Brazilian public healthcare workflows. The assistant should understand Brazilian Portuguese clinical language, SUS operational terminology, official protocol context, and structured triage-oriented outputs.

## Problem

General medical models often assume non-Brazilian contexts and fail to handle local language and operational workflows such as UBS, UPA, SAMU, regulation, CROSS-like vacancy workflows, acolhimento, classificacao de risco, and common Brazilian clinical shorthand.

Examples of important terms:

- PA 18x12
- dipirona EV
- vaga CROSS
- encaminhar para UBS
- regulacao
- SAMU
- UPA
- receituario azul
- classificacao de risco
- acolhimento

## Product Positioning

Use this positioning:

- Local-first clinical assistant for SUS workflows.
- Gemma 4 optimized for Brazilian healthcare workflows.
- Offline healthcare AI for underserved regions.
- Assistant adapted to SUS protocols and Brazilian Portuguese.

Avoid this positioning:

- ChatGPT medico.
- Automatic diagnosis.
- Better than MedGemma.
- Replacement for clinicians.

## Target Users

- Healthcare workers in UBS and UPA contexts.
- Administrative staff handling routing and orientation.
- Hackathon evaluators testing local-first AI for public health.
- Developers building SUS-aware AI workflows.

## Core Demo

The demo should accept a short Brazilian Portuguese case, retrieve relevant protocol snippets, call Gemma through Ollama, and return structured JSON plus a human-readable summary.

Example input:

```text
Paciente relata PA 18x12, cefaleia forte e falta de ar. Esta na UBS.
```

Example structured output:

```json
{
  "risk_level": "emergency",
  "summary": "Paciente com pressao arterial muito elevada associada a sintomas de alarme.",
  "suggested_action": "Encaminhar para atendimento de urgencia conforme fluxo local.",
  "referral": "UPA_or_emergency",
  "red_flags": ["falta de ar", "cefaleia forte", "pressao arterial muito elevada"],
  "sus_basis": ["Protocolo oficial recuperado via RAG"],
  "safety_notice": "Esta orientacao nao substitui avaliacao profissional. Acionar emergencia se houver piora."
}
```

## Success Criteria

- Responds in Brazilian Portuguese.
- Produces valid structured output.
- Uses SUS-specific pathways.
- Preserves safety boundaries.
- Works locally with Ollama.
- Supports a fine-tuning path without relying on memorized medical protocols.
