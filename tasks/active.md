# Active Tasks

## Current Task

Plan official RAG document ingestion and public dataset acquisition for the next MVP phase.

## Checklist

- [ ] Define RAG document acquisition policy and commit/storage rules.
- [ ] Select first official SUS documents for manual curation.
- [ ] Define dataset acquisition policy for public fine-tuning candidates.
- [ ] Add validation for official document manifest metadata before ingestion expansion.
- [ ] Run validation and open PR.

## Notes

- Prioritize official RAG documents before fine-tuning datasets.
- Keep PDFs or large raw files out of Git unless explicitly justified.
- Commit small curated Markdown/text extracts with source URLs and retrieval dates when they improve reproducible demo behavior.
- Keep downloaded datasets local/ignored until license, privacy, and schema checks pass.
