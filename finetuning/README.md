# Fine-Tuning

Fine-tuning assets for Gemma SUS Assistant. This track teaches behavior, Brazilian Portuguese style, SUS workflow formatting, safety boundaries, and structured JSON discipline. Protocol facts should remain in RAG unless explicitly reviewed and stable.

## Dataset Format

Datasets use JSONL. Each line is a `FineTuningExample`:

```json
{
  "id": "seed_001",
  "instruction": "Responda como assistente local-first para fluxos do SUS.",
  "input": "Caso sintetico em portugues brasileiro.",
  "context": "Contexto RAG opcional ou string vazia.",
  "output": {
    "risk_level": "low | moderate | high | emergency",
    "summary": "string",
    "suggested_action": "string",
    "referral": "UBS | UPA | SAMU | emergency | scheduled_follow_up | administrative_guidance | unknown",
    "red_flags": ["string"],
    "sus_basis": ["string"],
    "limitations": "string",
    "safety_notice": "string"
  },
  "tags": ["schema", "safety"],
  "split": "train | validation | safety",
  "source": "synthetic"
}
```

## Commands

Validate datasets:

```bash
python -m finetuning.scripts.validate_dataset
```

Preview the QLoRA skeleton:

```bash
python -m finetuning.scripts.train_qlora_skeleton --dry-run
```

## Rules

- Use synthetic or fully anonymized examples only.
- Do not train protocol details that should come from RAG.
- Include safety/refusal behavior and structured-output validity examples.
- Keep trained adapters in `finetuning/adapters/`, which is ignored locally until an export policy is defined.
- Follow `docs/dataset-acquisition.md` before downloading public datasets or deriving new training examples.
