# RAG Skill

## Purpose

Use this playbook for retrieval over official SUS documents and public healthcare materials.

## Practices

- Track document provenance, publisher, URL, and retrieval date.
- Chunk by semantic section when possible.
- Preserve citations through retrieval and rendering.
- Keep retrieval independent from generation.
- Evaluate retrieval quality with known protocol questions.
- Prefer official public sources.

## Anti-Patterns

- Treating retrieved snippets as automatically correct without source metadata.
- Mixing unofficial web content with official protocols without labeling.
- Fine-tuning protocol facts that should come from retrievable documents.
- Returning guidance without cited basis when protocol grounding is requested.

## Checklist

- [ ] Source metadata captured.
- [ ] Chunking strategy documented.
- [ ] Retrieval tests or evals exist.
- [ ] UI/API can show citations.
- [ ] Stale documents can be refreshed.
