from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

client = TestClient(app)


def test_health_returns_local_status() -> None:
    app.dependency_overrides.clear()
    get_settings.cache_clear()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "model_runtime": "mock",
        "rag_index": "not_configured",
    }
