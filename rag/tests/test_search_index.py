from rag.scripts.ingest_documents import DocumentChunk
from rag.scripts.search_index import index_chunks, search, tokenize


def chunk(chunk_id: str, section: str, text: str) -> DocumentChunk:
    return DocumentChunk(
        id=chunk_id,
        document_id="doc_1",
        source_id="source_1",
        title="Fluxo UBS UPA SAMU",
        section=section,
        text=text,
        source_url="https://example.test/doc",
        publisher="Ministerio da Saude",
        retrieved_at="2026-05-12",
        language="pt-BR",
    )


def test_tokenize_normalizes_portuguese_terms() -> None:
    assert tokenize("Atenção Básica, SAMU 192 e regulação") == [
        "atencao",
        "basica",
        "samu",
        "192",
        "e",
        "regulacao",
    ]


def test_tokenize_can_remove_portuguese_stopwords() -> None:
    assert tokenize("falta de ar na UPA", remove_stopwords=True) == ["falta", "ar", "upa"]


def test_search_returns_ranked_chunks_with_citations() -> None:
    indexed = index_chunks(
        [
            chunk("chunk_1", "Acolhimento", "UBS realiza acolhimento e acompanhamento."),
            chunk("chunk_2", "Sinais de alarme", "Falta de ar e dor no peito indicam UPA."),
        ]
    )

    results = search("falta de ar UPA", indexed)

    assert results[0].chunk_id == "chunk_2"
    assert results[0].source_url == "https://example.test/doc"
    assert results[0].publisher == "Ministerio da Saude"


def test_search_matches_accent_variants() -> None:
    indexed = index_chunks([chunk("chunk_1", "Regulação", "Encaminhamento na atenção básica.")])

    results = search("regulacao atencao basica", indexed)

    assert results[0].chunk_id == "chunk_1"


def test_search_boosts_title_and_section_terms() -> None:
    indexed = index_chunks(
        [
            chunk("chunk_1", "Acolhimento", "UPA."),
            chunk("chunk_2", "UPA", "Acolhimento local."),
        ]
    )

    results = search("UPA", indexed)

    assert results[0].chunk_id == "chunk_2"


def test_search_boosts_exact_phrase_matches() -> None:
    indexed = index_chunks(
        [
            chunk("chunk_1", "Sinais", "Falta e dor podem ser relatadas no acolhimento."),
            chunk("chunk_2", "Sinais", "Falta de ar deve ser avaliada com prioridade."),
        ]
    )

    results = search("falta de ar", indexed)

    assert results[0].chunk_id == "chunk_2"


def test_search_ignores_zero_score_chunks() -> None:
    indexed = index_chunks([chunk("chunk_1", "Acolhimento", "UBS e acolhimento.")])

    assert search("termo inexistente", indexed) == []
