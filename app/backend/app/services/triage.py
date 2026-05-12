import json

from pydantic import ValidationError

from app.model_runtime import ModelRuntime
from app.ollama_client import OllamaError
from app.schemas import Referral, RiskLevel, TriageResponse
from app.services.prompt_builder import build_triage_prompt

URGENT_TERMS = (
    "falta de ar",
    "dor toracica",
    "dor no peito",
    "desmaio",
    "convulsao",
    "pa 18x12",
    "pa 180",
)


async def create_triage_response(
    case_text: str,
    model_runtime: ModelRuntime | None,
) -> TriageResponse:
    if model_runtime is None:
        return create_mock_triage_response(case_text)

    try:
        generated = await model_runtime.generate(build_triage_prompt(case_text))
        response = TriageResponse.model_validate(json.loads(generated))
        response.runtime = "ollama"
        return response
    except (json.JSONDecodeError, OllamaError, ValidationError):
        fallback = create_mock_triage_response(case_text)
        fallback.runtime = "mock_fallback"
        return fallback


def create_mock_triage_response(case_text: str) -> TriageResponse:
    normalized = case_text.lower()
    red_flags = [term for term in URGENT_TERMS if term in normalized]

    if red_flags:
        return TriageResponse(
            risk_level=RiskLevel.EMERGENCY,
            summary="Caso com sinais de alarme relatados e necessidade de avaliacao urgente.",
            suggested_action="Encaminhar para atendimento de urgencia conforme fluxo local do SUS.",
            referral=Referral.UPA,
            red_flags=red_flags,
            sus_basis=["Resposta mockada do app shell; RAG oficial ainda nao configurado."],
            limitations="Esta orientacao nao substitui avaliacao de profissional de saude.",
            safety_notice=(
                "Se houver piora, falta de ar, dor no peito, confusao ou desmaio, "
                "acionar SAMU 192 ou procurar emergencia."
            ),
            runtime="mock",
        )

    return TriageResponse(
        risk_level=RiskLevel.MODERATE,
        summary="Caso recebido para orientacao inicial no fluxo SUS.",
        suggested_action=(
            "Procurar avaliacao em UBS ou acolhimento local, conforme disponibilidade "
            "e evolucao dos sintomas."
        ),
        referral=Referral.UBS,
        red_flags=[],
        sus_basis=["Resposta mockada do app shell; RAG oficial ainda nao configurado."],
        limitations="Esta orientacao nao substitui avaliacao de profissional de saude.",
        safety_notice=(
            "Buscar UPA, emergencia ou SAMU 192 se surgirem sinais de alarme "
            "ou piora importante."
        ),
        runtime="mock",
    )
