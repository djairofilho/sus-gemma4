# Data Model

## Current Policy

The initial product should avoid persistent patient data storage. Store only development fixtures, public documents, indexes, and non-identifiable eval examples.

## Planned Entities

### Document

- `id`: stable identifier.
- `title`: source title.
- `source_url`: official URL when available.
- `publisher`: source organization.
- `published_at`: optional publication date.
- `retrieved_at`: ingestion date.
- `license`: usage notes when known.
- `local_path`: local file reference.

### SourceRegistryEntry

- `id`: stable source identifier.
- `name`: source display name.
- `category`: source category for official RAG sources.
- `publisher`: publishing organization for official sources.
- `base_url`: HTTPS source root.
- `scope`: federal, state, municipal, regional, or restricted scope.
- `use`: rag, structured_context, terminology_normalization, benchmark, or SFT use.
- `access`: public, public_or_research, or restricted.
- `citation_required`: true for official RAG sources.
- `contains_patient_data`: true only for restricted future datasets with credentialing.
- `requires_credentialing`: true for restricted or patient-data sources.
- `notes`: operational and safety notes in Brazilian Portuguese or English.

### Chunk

- `id`: stable chunk identifier.
- `document_id`: parent document.
- `section`: heading or section path.
- `text`: chunk text.
- `embedding_id`: optional vector reference.
- `metadata`: source metadata.

### EvalCase

- `id`: stable case identifier.
- `input`: non-identifiable input.
- `expected_properties`: expected safety/schema properties.
- `tags`: terminology, risk level, pathway, regression group.
- `source`: synthetic, public, or expert-authored.

### FineTuningExample

- `id`: stable example identifier.
- `instruction`: user or system instruction.
- `input`: scenario text.
- `context`: optional RAG-like context.
- `output`: target structured response.
- `tags`: safety, pathway, terminology, schema.
- `split`: train, validation, or test.

## Privacy Rules

- Do not commit real patient identifiers.
- Do not store raw operational data in the repository.
- Use synthetic or fully anonymized examples only.
- Add an ADR before adding persistence for user-submitted cases.
