from rag.scripts.ingest_documents import (
    DocumentManifestEntry,
    chunk_document,
    ingest_documents,
    normalize_text,
    split_markdown_sections,
)


def manifest_entry() -> DocumentManifestEntry:
    return DocumentManifestEntry(
        id="doc_1",
        source_id="source_1",
        title="Documento teste",
        source_url="https://example.test/doc",
        publisher="Ministerio da Saude",
        retrieved_at="2026-05-12",
        license="synthetic_fixture_for_tests",
        language="pt-BR",
        local_path="rag/documents/raw/doc.md",
        notes="Teste.",
    )


def test_split_markdown_sections_uses_headings() -> None:
    sections = split_markdown_sections("# Titulo\n\n## UBS\nTexto UBS.\n## UPA\nTexto UPA.")

    assert sections == [
        {"section": "Titulo", "text": ""},
        {"section": "UBS", "text": "Texto UBS."},
        {"section": "UPA", "text": "Texto UPA."},
    ]


def test_normalize_text_collapses_whitespace() -> None:
    assert normalize_text("Texto\n\n com   espacos") == "Texto com espacos"


def test_chunk_document_preserves_citation_metadata() -> None:
    chunks = chunk_document(
        manifest_entry(),
        "# Documento\n\n## Sinais de alarme\nFalta de ar e dor no peito.",
    )

    assert len(chunks) == 1
    assert chunks[0].id == "doc_1::chunk_0002"
    assert chunks[0].section == "Sinais de alarme"
    assert chunks[0].source_url == "https://example.test/doc"
    assert chunks[0].language == "pt-BR"


def test_ingest_documents_includes_curated_official_extracts() -> None:
    chunks = ingest_documents()
    document_ids = {chunk.document_id for chunk in chunks}

    assert "official_linhas_cuidado_overview" in document_ids
    assert "official_bvsms_overview" in document_ids
    assert "official_pcdt_overview" in document_ids
    assert "official_rename_medicines_overview" in document_ids
    assert "official_bvsms_referral_search_overview" in document_ids
