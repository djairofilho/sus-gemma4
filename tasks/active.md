# Active Tasks

## Current Task

Finalize local RAG retrieval.

## Checklist

- [x] Confirm official protocol extracts are complete for the MVP scope.
- [x] Add local sparse vector embeddings to the generated RAG index.
- [x] Keep deterministic lexical scoring as fallback inside hybrid retrieval.
- [x] Keep fine-tuning dataset acquisition and training deferred.
- [x] Run validation.

## Notes

- Raw downloads are local and ignored; do not commit downloaded HTML/PDF files.
- Commit only small curated Markdown/text extracts with manifest provenance.
- Prefer complete official protocol or pathway pages over overview pages for protocol-specific guidance.
- Do not infer protocol-specific conduct beyond the cited official text.
- Fine-tuning validation is opt-in during this RAG release pass with `GEMMA_SUS_VALIDATE_FINETUNING=true`.
