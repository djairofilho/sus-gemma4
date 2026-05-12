# Active Tasks

## Current Task

Download official public RAG source pages locally and derive curated SUS extracts.

## Checklist

- [x] Create ignored local raw download area.
- [x] Register official RAG page downloads in `data/sources/rag_downloads.yml`.
- [x] Download official source pages into `data/raw/public/rag/`.
- [x] Add condition/pathway-specific curated extracts from downloaded pages.
- [x] Add retrieval evals for priority SUS queries.
- [ ] Run validation and open PR.

## Notes

- Raw downloads are local and ignored; do not commit downloaded HTML/PDF files.
- Commit only small curated Markdown/text extracts with manifest provenance.
- Do not infer protocol-specific conduct from overview pages alone.
- Downloaded local HTML files are recorded in `data/sources/rag_downloads.yml` but intentionally ignored by Git.
