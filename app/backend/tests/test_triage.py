import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import TriageResponse
from app.services.triage import create_triage_response

client = TestClient(app)


def test_triage_returns_schema_valid_response() -> None:
    response = client.post("/api/triage", json={"case_text": "Paciente com febre e tosse."})

    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "moderate"
    assert body["referral"] == "UBS"
    assert body["red_flags"] == []
    assert body["runtime"] == "mock"
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


class FakeRuntime:
    async def generate(self, prompt: str) -> str:
        response = TriageResponse(
            risk_level="low",
            summary="Resposta validada pelo runtime fake.",
            suggested_action="Orientar acompanhamento na UBS.",
            referral="UBS",
            red_flags=[],
            sus_basis=["Runtime fake em teste."],
            limitations="Nao substitui avaliacao profissional.",
            safety_notice="Buscar atendimento se houver piora.",
        )
        return response.model_dump_json()


class InvalidRuntime:
    async def generate(self, prompt: str) -> str:
        return "nao-json"


def test_triage_uses_runtime_response_when_valid() -> None:
    response = client.post("/api/triage", json={"case_text": "Caso simples."})

    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_triage_response_uses_valid_runtime() -> None:
    response = await create_triage_response("Caso simples.", FakeRuntime())

    assert response.runtime == "ollama"
    assert response.summary == "Resposta validada pelo runtime fake."


@pytest.mark.anyio
async def test_create_triage_response_falls_back_on_invalid_runtime() -> None:
    response = await create_triage_response("Paciente com falta de ar.", InvalidRuntime())

    assert response.runtime == "mock_fallback"
    assert response.risk_level == "emergency"
