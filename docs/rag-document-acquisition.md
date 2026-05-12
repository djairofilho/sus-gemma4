# RAG Document Acquisition

## Goal

Acquire official SUS-oriented documents for local RAG without adding hidden network calls, private data, or unclear provenance.

## Priority Sources

Start with small curated Markdown/text extracts from these official sources:

1. Linhas de Cuidado do Ministerio da Saude: `ministerio_saude_linhas_cuidado`.
2. Protocolos da Atencao Basica / BVS MS: `ministerio_saude_protocolos_atencao_basica`.
3. Protocolos de Encaminhamento: `ministerio_saude_protocolos_encaminhamento`.
4. PCDT only when needed for a demo case: `ministerio_saude_pcdt`.

## Storage Policy

- Commit small curated Markdown/text extracts when they improve reproducibility and demo behavior.
- Keep large PDFs, downloaded archives, and raw bulk exports out of Git unless a PR explicitly justifies them.
- Store local-only downloads under ignored paths until curated.
- Do not commit private clinical records, patient identifiers, local service spreadsheets, or operational exports.

## Curation Rules

- Prefer official federal sources before state or municipal material.
- Preserve `source_url`, publisher, retrieval date, license/usage note, language, and local path in `rag/documents/manifest.yml`.
- Keep text in Brazilian Portuguese when the source is Brazilian public material.
- Curated extracts must not claim to be complete protocols unless they contain the complete reviewed document.
- Generated guidance must cite retrieved context in `sus_basis` when protocol grounding is used.

## Manual Workflow

1. Select a registered source from `data/sources/official_sources.yml`.
2. Download or copy the official document manually.
3. Create a small Markdown/text extract in `rag/documents/raw/`.
4. Add manifest metadata to `rag/documents/manifest.yml`.
5. Run `python -m rag.scripts.validate_sources`.
6. Run `python -m rag.scripts.ingest_documents`.
7. Run `python -m rag.scripts.search_index --build`.
8. Add or update retrieval tests for expected SUS terminology.

## First Retrieval Questions

- `falta de ar dor no peito UPA SAMU`
- `acolhimento UBS sem sinais de alarme`
- `encaminhamento especialista regulacao atencao basica`
- `receituario azul medicamento controlado UBS`
