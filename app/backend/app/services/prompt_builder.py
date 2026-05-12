from app.schemas import Referral, RiskLevel


def build_triage_prompt(case_text: str) -> str:
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
""".strip()
