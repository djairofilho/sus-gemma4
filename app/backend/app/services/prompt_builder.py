from app.schemas import RagSearchResult, Referral, RiskLevel


def build_triage_prompt(case_text: str, rag_context: list[RagSearchResult] | None = None) -> str:
    risk_values = ", ".join(level.value for level in RiskLevel)
    referral_values = ", ".join(referral.value for referral in Referral)

    return f"""
Voce e um assistente local-first para fluxos do SUS brasileiro.
Responda somente JSON valido, sem Markdown.

Regras de seguranca:
- Nao forneca diagnostico definitivo.
- Nao prescreva medicamentos controlados.
- Oriente emergencia, UPA ou SAMU 192 em sinais de alarme.
- Declare que a orientacao nao substitui avaliacao profissional.

Valores permitidos para risk_level: {risk_values}.
Valores permitidos para referral: {referral_values}.

Schema esperado:
{{
  "risk_level": "low | moderate | high | emergency",
  "summary": "string",
  "suggested_action": "string",
  "referral": "UBS | UPA | SAMU | emergency | scheduled_follow_up | "
  "administrative_guidance | unknown",
  "red_flags": ["string"],
  "sus_basis": ["string"],
  "limitations": "string",
  "safety_notice": "string"
}}

Caso:
{case_text}

Contexto RAG recuperado:
{format_rag_context(rag_context or [])}
""".strip()


def build_triage_repair_prompt(invalid_output: str) -> str:
    return f"""
A resposta anterior nao seguiu o JSON esperado.
Converta a resposta abaixo para somente JSON valido, sem Markdown e sem texto adicional.
Preserve orientacao conservadora, limites de seguranca e valores permitidos do schema.

Resposta anterior:
{invalid_output}
""".strip()


def format_rag_context(rag_context: list[RagSearchResult]) -> str:
    if not rag_context:
        return "Nenhum contexto RAG recuperado."

    return "\n\n".join(
        (
            f"Fonte: {result.title} | Secao: {result.section} | "
            f"Publisher: {result.publisher} | URL: {result.source_url}\n"
            f"Trecho: {result.text}"
        )
        for result in rag_context
    )
