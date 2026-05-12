from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app
from app.services import rag_search

client = TestClient(app)


def test_health_returns_local_status(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    app.dependency_overrides.clear()
    get_settings.cache_clear()
    monkeypatch.setattr(rag_search, "INDEX_PATH", tmp_path / "missing_index.jsonl")

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "model_runtime": "mock",
        "rag_index": "not_built",
    }


def test_health_reports_ready_rag_index(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    index_path = tmp_path / "lexical_index.jsonl"
    index_path.write_text("", encoding="utf-8")
    monkeypatch.setattr(rag_search, "INDEX_PATH", index_path)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["rag_index"] == "ready"
