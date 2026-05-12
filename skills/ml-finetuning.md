# ML Fine-Tuning Skill

## Purpose

Use this playbook for Unsloth, LoRA/QLoRA, dataset design, training scripts, adapter export, and model evals.

## Practices

- Fine-tune behavior, language, structure, and workflow style.
- Keep medical/protocol facts in RAG unless stable and generic.
- Use synthetic or anonymized examples only.
- Maintain train/validation/test splits.
- Include refusal and safety examples.
- Evaluate structured output validity after training.

## Anti-Patterns

- Training on real patient data.
- Training the model to memorize protocols instead of using RAG.
- Using unsafe examples without correction targets.
- Judging adapters only by subjective output quality.
- Publishing adapters without dataset and eval documentation.

## Checklist

- [ ] Dataset format documented.
- [ ] No identifiable data.
- [ ] Safety examples included.
- [ ] JSON validity eval included.
- [ ] Adapter export path documented.
