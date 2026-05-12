import json

from pydantic import ValidationError

from app.schemas import TriageResponse


class StructuredOutputError(ValueError):
    pass


def parse_triage_response(raw_output: str) -> TriageResponse:
    candidate = extract_json_object(raw_output)

    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as error:
        raise StructuredOutputError("Model output is not valid JSON") from error

    try:
        return TriageResponse.model_validate(payload)
    except ValidationError as error:
        raise StructuredOutputError("Model output does not match triage schema") from error


def extract_json_object(raw_output: str) -> str:
    stripped = raw_output.strip()
    if not stripped:
        raise StructuredOutputError("Model output is empty")

    without_fence = strip_markdown_fence(stripped)
    if without_fence.startswith("{") and without_fence.endswith("}"):
        return without_fence

    start = without_fence.find("{")
    if start == -1:
        raise StructuredOutputError("Model output does not contain a JSON object")

    depth = 0
    in_string = False
    escaped = False

    for index, char in enumerate(without_fence[start:], start=start):
        if escaped:
            escaped = False
            continue

        if char == "\\" and in_string:
            escaped = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return without_fence[start : index + 1]

    raise StructuredOutputError("Model output contains an incomplete JSON object")


def strip_markdown_fence(raw_output: str) -> str:
    lines = raw_output.strip().splitlines()
    if len(lines) >= 3 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()

    return raw_output.strip()
