from app.model_runtime import ModelRuntime
from app.schemas import RagSearchResult, Referral, RiskLevel, TriageResponse
from app.services.prompt_builder import build_triage_prompt, build_triage_repair_prompt
from app.services.structured_output import StructuredOutputError, parse_triage_response

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
    rag_context: list[RagSearchResult] | None = None,
) -> TriageResponse:
    if model_runtime is None:
        return create_mock_triage_response(case_text, rag_context=rag_context)

    generated = ""
    try:
        generated = await model_runtime.generate(build_triage_prompt(case_text, rag_context))
        response = parse_triage_response(generated)
    except StructuredOutputError:
        try:
            repaired = await model_runtime.generate(build_triage_repair_prompt(generated))
            response = parse_triage_response(repaired)
        except (RuntimeError, StructuredOutputError):
            fallback = create_mock_triage_response(case_text, rag_context=rag_context)
            fallback.runtime = "mock_fallback"
            return fallback
    except RuntimeError:
        fallback = create_mock_triage_response(case_text, rag_context=rag_context)
        fallback.runtime = "mock_fallback"
        return fallback

    response.runtime = "ollama"
    return response


def create_mock_triage_response(
    case_text: str,
    rag_context: list[RagSearchResult] | None = None,
) -> TriageResponse:
    normalized = case_text.lower()
    red_flags = [term for term in URGENT_TERMS if term in normalized]
    sus_basis = format_sus_basis(rag_context)

    if red_flags:
        return TriageResponse(
            risk_level=RiskLevel.EMERGENCY,
            summary="Caso com sinais de alarme relatados e necessidade de avaliacao urgente.",
            suggested_action="Encaminhar para atendimento de urgencia conforme fluxo local do SUS.",
            referral=Referral.UPA,
            red_flags=red_flags,
            sus_basis=sus_basis,
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
        sus_basis=sus_basis,
        limitations="Esta orientacao nao substitui avaliacao de profissional de saude.",
        safety_notice=(
            "Buscar UPA, emergencia ou SAMU 192 se surgirem sinais de alarme "
            "ou piora importante."
        ),
        runtime="mock",
    )


def format_sus_basis(rag_context: list[RagSearchResult] | None) -> list[str]:
    if not rag_context:
        return ["Resposta mockada; nenhum contexto RAG recuperado."]

    return [f"{item.title} - {item.section}: {item.source_url}" for item in rag_context]
