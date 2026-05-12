import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import RagSearchResult, Referral, RiskLevel, TriageResponse
from app.services.triage import create_triage_response

client = TestClient(app)


def rag_result() -> RagSearchResult:
    return RagSearchResult(
        chunk_id="chunk_1",
        score=3,
        title="Fluxo UBS UPA SAMU",
        section="Sinais de alarme",
        text="Falta de ar e dor no peito indicam encaminhamento para urgencia.",
        source_url="https://example.test/fluxo",
        publisher="Ministerio da Saude",
    )


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


def test_triage_uses_retrieved_rag_basis(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.main.search_rag", lambda query: [rag_result()])

    response = client.post(
        "/api/triage",
        json={"case_text": "Paciente com dor no peito e falta de ar."},
    )

    assert response.status_code == 200
    assert response.json()["sus_basis"] == [
        "Fluxo UBS UPA SAMU - Sinais de alarme: https://example.test/fluxo"
    ]


def test_triage_rejects_empty_case_text() -> None:
    response = client.post("/api/triage", json={"case_text": ""})

    assert response.status_code == 422


class FakeRuntime:
    calls = 0

    async def generate(self, prompt: str) -> str:
        self.calls += 1
        response = TriageResponse(
            risk_level=RiskLevel.LOW,
            summary="Resposta validada pelo runtime fake.",
            suggested_action="Orientar acompanhamento na UBS.",
            referral=Referral.UBS,
            red_flags=[],
            sus_basis=["Runtime fake em teste."],
            limitations="Nao substitui avaliacao profissional.",
            safety_notice="Buscar atendimento se houver piora.",
        )
        return response.model_dump_json()


class InvalidRuntime:
    async def generate(self, prompt: str) -> str:
        return "nao-json"


class RepairableRuntime:
    def __init__(self) -> None:
        self.calls = 0

    async def generate(self, prompt: str) -> str:
        self.calls += 1
        if self.calls == 1:
            return "A resposta e moderada, encaminhar UBS."

        response = TriageResponse(
            risk_level=RiskLevel.MODERATE,
            summary="Resposta corrigida apos retry.",
            suggested_action="Orientar avaliacao na UBS.",
            referral=Referral.UBS,
            red_flags=[],
            sus_basis=["Runtime fake em retry."],
            limitations="Nao substitui avaliacao profissional.",
            safety_notice="Buscar atendimento se houver piora.",
        )
        return response.model_dump_json()


def test_triage_uses_runtime_response_when_valid() -> None:
    response = client.post("/api/triage", json={"case_text": "Caso simples."})

    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_triage_response_uses_valid_runtime() -> None:
    runtime = FakeRuntime()
    response = await create_triage_response("Caso simples.", runtime)

    assert response.runtime == "ollama"
    assert response.summary == "Resposta validada pelo runtime fake."
    assert runtime.calls == 1


@pytest.mark.anyio
async def test_create_triage_response_repairs_invalid_runtime_output() -> None:
    runtime = RepairableRuntime()
    response = await create_triage_response("Caso simples.", runtime)

    assert response.runtime == "ollama"
    assert response.summary == "Resposta corrigida apos retry."
    assert runtime.calls == 2


@pytest.mark.anyio
async def test_create_triage_response_falls_back_on_invalid_runtime() -> None:
    response = await create_triage_response("Paciente com falta de ar.", InvalidRuntime())

    assert response.runtime == "mock_fallback"
    assert response.risk_level == "emergency"


@pytest.mark.anyio
async def test_create_triage_response_passes_rag_context_to_prompt() -> None:
    runtime = FakeRuntime()
    response = await create_triage_response(
        "Paciente com falta de ar.",
        runtime,
        rag_context=[rag_result()],
    )

    assert response.runtime == "ollama"
    assert runtime.calls == 1
