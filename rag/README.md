# RAG

Local retrieval foundation for official SUS-oriented sources.

## Current Scope

This module currently defines local document layout and source metadata validation. It does not download, scrape, embed, or index documents yet.

## Pipeline

```text
source registry
  -> raw official documents
  -> processed text
  -> semantic chunks
  -> local index
  -> cited retrieval
  -> prompt context
```

## Layout

- `documents/raw`: original official files or manually downloaded public documents.
- `documents/processed`: cleaned text and metadata derived from raw files.
- `index`: local retrieval indexes generated from processed chunks.
- `scripts`: validation and future ingestion scripts.
- `tests`: tests for source metadata and retrieval behavior.

## Rules

- Preserve source URL, publisher, scope, access mode, and citation requirement.
- Do not store private clinical records.
- Do not mix RAG official sources with fine-tuning datasets.
- RAG content and citations should be in Brazilian Portuguese when sourced from Brazilian public materials.
