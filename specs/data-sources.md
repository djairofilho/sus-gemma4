# Data Sources Spec

## Purpose

Define allowed source categories for RAG, fine-tuning, benchmarking, and structured public data. Technical schema keys remain in English; source content, examples, prompts, and generated clinical-administrative text should be Brazilian Portuguese.

## Source Categories

### RAG Official Sources

Use RAG for official, citeable, and update-sensitive knowledge:

- PCDT from Ministerio da Saude.
- Linhas de Cuidado from Ministerio da Saude.
- Protocolos da Atencao Basica.
- Protocolos de Encaminhamento da Atencao Basica para Atencao Especializada.
- RENAME.
- CONITEC recommendations, PCDT, reports, and health technology assessments.
- BVS MS.
- DeCS/MeSH and Terminologia da Saude for term normalization.
- Open DataSUS, DataSUS, and CNES for structured context and territorial metadata.

### Fine-Tuning And Benchmark Sources

Use fine-tuning for behavior, format, language, refusal patterns, terminology, and structured output discipline. Do not use fine-tuning as the primary store for protocols that should be retrieved through RAG.

Candidate sources:

- MedPT.
- HealthQA-BR.
- MedReason-BR.
- SemClinBr.
- e-NatJus v2.
- BRATECA, only as a future restricted research source with credentialing and privacy review.

## Governance Rules

- Do not commit identifiable patient data.
- Do not train on real medical records without authorization, deidentification, and an ADR.
- Cite RAG sources in `sus_basis` when protocol guidance is used.
- Keep RAG source metadata separate from fine-tuning source metadata.
- Label restricted or credentialed datasets explicitly.
- Prefer official federal sources before state or municipal sources for hackathon MVP.
- Use synthetic supervised examples only when they are traceable to allowed behavior requirements or official source context.
- Keep large raw downloads and public dataset archives out of Git until a PR explicitly justifies committing them.
- Commit curated RAG Markdown/text extracts only when manifest metadata preserves official source provenance and retrieval date.
- Acquire public fine-tuning datasets for review before training; do not train on downloaded data until license, privacy, and schema checks pass.

## Acquisition Guides

- RAG documents: `docs/rag-document-acquisition.md`.
- Fine-tuning and benchmark datasets: `docs/dataset-acquisition.md`.

## Schema Language Policy

Keep API and model-output field names in English:

- `risk_level`
- `referral`
- `summary`
- `suggested_action`
- `sus_basis`
- `red_flags`
- `limitations`
- `safety_notice`

Keep user-facing field values in Brazilian Portuguese, including clinical-administrative terms such as UBS, UPA, SAMU, acolhimento, regulacao, classificacao de risco, receituario azul, and encaminhamento.
