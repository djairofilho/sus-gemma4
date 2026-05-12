from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_triage_returns_schema_valid_response() -> None:
    response = client.post("/api/triage", json={"case_text": "Paciente com febre e tosse."})

    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "moderate"
    assert body["referral"] == "UBS"
    assert body["red_flags"] == []
    assert "nao substitui" in body["limitations"]


def test_triage_escalates_mock_red_flags() -> None:
    response = client.post(
        "/api/triage",
        json={"case_text": "Paciente com PA 18x12, dor no peito e falta de ar."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "emergency"
    assert body["referral"] == "UPA"
    assert "falta de ar" in body["red_flags"]
    assert "dor no peito" in body["red_flags"]


def test_triage_rejects_empty_case_text() -> None:
    response = client.post("/api/triage", json={"case_text": ""})

    assert response.status_code == 422
