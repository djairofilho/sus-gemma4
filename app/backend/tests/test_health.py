from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_local_status() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "model_runtime": "ollama_not_connected",
        "rag_index": "not_configured",
    }
