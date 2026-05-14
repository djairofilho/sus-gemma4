import pytest

from rag.scripts.ingest_documents import DocumentChunk
from rag.scripts.search_index import cosine_similarity, index_chunks, normalize_vector, search, tokenize


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


def test_index_chunks_adds_local_vector_embeddings() -> None:
    indexed = index_chunks([chunk("chunk_1", "Sinais", "Falta de ar indica UPA.")])

    assert indexed[0].vector
    assert cosine_similarity(normalize_vector({"falta": 1, "ar": 1}), indexed[0].vector) > 0


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


def test_search_finds_curated_official_extracts() -> None:
    from rag.scripts.ingest_documents import ingest_documents

    indexed = index_chunks(ingest_documents())
    results = search("linhas de cuidado atencao primaria", indexed)

    assert any(result.chunk_id.startswith("official_linhas_cuidado_overview") for result in results)


def test_search_finds_medicine_safety_extract() -> None:
    from rag.scripts.ingest_documents import ingest_documents

    indexed = index_chunks(ingest_documents())
    results = search("receituario azul medicamento controlado prescricao UBS", indexed)

    assert any(
        result.chunk_id.startswith("official_rename_medicines_overview") for result in results
    )


def test_search_finds_referral_discovery_extract() -> None:
    from rag.scripts.ingest_documents import ingest_documents

    indexed = index_chunks(ingest_documents())
    results = search("encaminhamento especialista regulacao atencao basica", indexed)

    assert any(
        result.chunk_id.startswith("official_bvsms_referral_search_overview")
        for result in results
    )


@pytest.mark.parametrize(
    ("query", "document_id"),
    [
        ("crise hipertensiva lesao orgao alvo samu upa", "official_has_upa_flow"),
        ("hiperglicemia sintomatica diabetes samu emergencia", "official_dm2_upa_flow"),
        (
            "dengue dor barriga vomitos sangramento dificuldade respirar",
            "official_dengue_warning_signs",
        ),
        (
            "pre natal atencao primaria 12 semana consultas gestante",
            "official_pre_natal_aps_followup",
        ),
        ("ansiedade situacoes agudas upa samu caps raps", "official_anxiety_upa_raps_flow"),
    ],
)
def test_search_finds_priority_protocol_extracts(query: str, document_id: str) -> None:
    from rag.scripts.ingest_documents import ingest_documents

    indexed = index_chunks(ingest_documents())
    results = search(query, indexed)

    assert any(result.chunk_id.startswith(document_id) for result in results)


def test_search_ignores_zero_score_chunks() -> None:
    indexed = index_chunks([chunk("chunk_1", "Acolhimento", "UBS e acolhimento.")])

    assert search("termo inexistente", indexed) == []
