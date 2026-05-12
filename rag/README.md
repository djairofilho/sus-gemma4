# RAG

Local retrieval foundation for official SUS-oriented sources.

## Current Scope

This module currently supports local source metadata validation, local Markdown/text ingestion, section-based chunking, and a simple lexical search index. It does not download or scrape documents.

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

## Commands

Validate source registries:

```bash
python -m rag.scripts.validate_sources
```

Ingest local documents into processed chunks:

```bash
python -m rag.scripts.ingest_documents
```

Build the lexical index:

```bash
python -m rag.scripts.search_index --build
```

Search the local index:

```bash
python -m rag.scripts.search_index --query "falta de ar UPA"
```

## Rules

- Preserve source URL, publisher, scope, access mode, and citation requirement.
- Do not store private clinical records.
- Do not mix RAG official sources with fine-tuning datasets.
- RAG content and citations should be in Brazilian Portuguese when sourced from Brazilian public materials.
- Generated `*.jsonl` chunk and index artifacts are local build outputs and should not be committed.
