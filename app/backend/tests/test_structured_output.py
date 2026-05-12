import json

import pytest

from app.services.structured_output import StructuredOutputError, parse_triage_response


def valid_payload() -> dict[str, object]:
    return {
        "risk_level": "moderate",
        "summary": "Caso recebido para orientacao inicial.",
        "suggested_action": "Procurar UBS para avaliacao.",
        "referral": "UBS",
        "red_flags": [],
        "sus_basis": ["Teste"],
        "limitations": "Nao substitui avaliacao profissional.",
        "safety_notice": "Buscar atendimento se houver piora.",
    }


def test_parse_triage_response_accepts_plain_json() -> None:
    response = parse_triage_response(json.dumps(valid_payload()))

    assert response.risk_level == "moderate"
    assert response.referral == "UBS"


def test_parse_triage_response_accepts_markdown_fenced_json() -> None:
    raw_output = f"```json\n{json.dumps(valid_payload())}\n```"

    response = parse_triage_response(raw_output)

    assert response.summary == "Caso recebido para orientacao inicial."


def test_parse_triage_response_extracts_json_with_surrounding_text() -> None:
    raw_output = f"Aqui esta:\n{json.dumps(valid_payload())}\nFim."

    response = parse_triage_response(raw_output)

    assert response.safety_notice == "Buscar atendimento se houver piora."


def test_parse_triage_response_rejects_invalid_json() -> None:
    with pytest.raises(StructuredOutputError):
        parse_triage_response("{invalid-json")


def test_parse_triage_response_rejects_schema_errors() -> None:
    payload = valid_payload()
    payload["risk_level"] = "critical"

    with pytest.raises(StructuredOutputError):
        parse_triage_response(json.dumps(payload))
