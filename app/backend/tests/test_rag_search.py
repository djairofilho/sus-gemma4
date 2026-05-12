import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import RagSearchResult

client = TestClient(app)


def result() -> RagSearchResult:
    return RagSearchResult(
        chunk_id="chunk_1",
        score=4,
        title="Fluxo UBS UPA SAMU",
        section="Sinais de alarme",
        text="Falta de ar e dor no peito indicam encaminhamento para urgencia.",
        source_url="https://example.test/fluxo",
        publisher="Ministerio da Saude",
    )


def test_rag_search_returns_results(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.main.search_rag", lambda query, limit: [result()])

    response = client.post("/api/rag/search", json={"query": "falta de ar", "limit": 1})

    assert response.status_code == 200
    assert response.json() == {"results": [result().model_dump()]}


def test_rag_search_rejects_short_query() -> None:
    response = client.post("/api/rag/search", json={"query": "a"})

    assert response.status_code == 422
