# Dataset Acquisition

## Goal

Acquire public fine-tuning and benchmark candidates safely, without training on sensitive data or encoding protocol facts that belong in RAG.

## Priority Order

1. Use official RAG documents first for protocol knowledge and citations.
2. Catalog public dataset candidates locally for license and privacy review.
3. Extract only synthetic, anonymized, or behavior-oriented examples into committed JSONL datasets.
4. Run QLoRA training only after dataset validation and safety eval coverage are expanded.

## Candidate Sources

- MedPT: behavior/language candidate.
- HealthQA-BR: benchmark and light SFT candidate.
- MedReason-BR: reasoning-style evaluation candidate.
- SemClinBr: terminology/entity candidate.
- e-NatJus v2: health technology and medico-legal language candidate.
- BRATECA: restricted future research only, requiring credentialing, deidentification, authorization, and ADR.

## Storage Policy

- Keep raw downloaded datasets out of Git.
- Use ignored local storage for raw or intermediate data.
- Commit only reviewed JSONL examples that pass `python -m finetuning.scripts.validate_dataset`.
- Committed examples must use `source: "synthetic"` unless a future ADR defines another allowed source class.
- Do not commit names, CNS, CPF, phone numbers, addresses, record IDs, or real clinical narratives.

## Review Checklist

- License permits the intended research or demo use.
- Dataset language is Brazilian Portuguese or relevant to SUS terminology.
- No identifiable patient data is present in committed examples.
- Examples teach format, safety, refusal, routing, or terminology rather than memorized protocol facts.
- Safety and schema evals are updated before any real adapter is treated as useful.

## Manual Workflow

1. Register or verify the candidate in `data/sources/finetuning_sources.yml`.
2. Download raw data into a local ignored path.
3. Review license, access, and patient-data risk.
4. Derive synthetic or anonymized examples into `finetuning/datasets/*.jsonl`.
5. Run `python -m finetuning.scripts.validate_dataset`.
6. Run `bash scripts/validate.sh`.
