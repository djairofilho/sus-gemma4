from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = ROOT / "finetuning" / "datasets"
DEFAULT_DATASETS = (
    DATASET_DIR / "seed.jsonl",
    DATASET_DIR / "validation.jsonl",
    DATASET_DIR / "safety.jsonl",
)
REQUIRED_FIELDS = {"id", "instruction", "input", "context", "output", "tags", "split", "source"}
OUTPUT_FIELDS = {
    "risk_level",
    "summary",
    "suggested_action",
    "referral",
    "red_flags",
    "sus_basis",
    "limitations",
    "safety_notice",
}
RISK_LEVELS = {"low", "moderate", "high", "emergency"}
REFERRALS = {
    "UBS",
    "UPA",
    "SAMU",
    "emergency",
    "scheduled_follow_up",
    "administrative_guidance",
    "unknown",
}
SPLITS = {"train", "validation", "safety"}
FORBIDDEN_PATIENT_FIELDS = {"cpf", "cns", "rg", "address", "phone", "email", "nome", "name"}


@dataclass(frozen=True)
class DatasetFailure:
    path: Path
    line_number: int
    example_id: str
    reason: str


def load_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    examples: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"{path}:{line_number} must be a JSON object")
        examples.append((line_number, payload))
    return examples


def validate_dataset(path: Path) -> list[DatasetFailure]:
    failures: list[DatasetFailure] = []
    seen_ids: set[str] = set()
    for line_number, example in load_jsonl(path):
        example_id = str(example.get("id", "unknown"))
        failures.extend(validate_example(path, line_number, example_id, example, seen_ids))
    return failures


def validate_example(
    path: Path,
    line_number: int,
    example_id: str,
    example: dict[str, Any],
    seen_ids: set[str],
) -> list[DatasetFailure]:
    failures: list[DatasetFailure] = []
    missing = sorted(REQUIRED_FIELDS - set(example))
    failures.extend(failure(path, line_number, example_id, f"missing field: {field}") for field in missing)

    if example_id in seen_ids:
        failures.append(failure(path, line_number, example_id, "duplicate id"))
    seen_ids.add(example_id)

    if example.get("split") not in SPLITS:
        failures.append(failure(path, line_number, example_id, "invalid split"))

    if example.get("source") != "synthetic":
        failures.append(failure(path, line_number, example_id, "source must be synthetic for committed examples"))

    for field in FORBIDDEN_PATIENT_FIELDS:
        if field in example:
            failures.append(failure(path, line_number, example_id, f"forbidden patient field: {field}"))

    output = example.get("output")
    if not isinstance(output, dict):
        failures.append(failure(path, line_number, example_id, "output must be an object"))
        return failures

    missing_output = sorted(OUTPUT_FIELDS - set(output))
    failures.extend(
        failure(path, line_number, example_id, f"missing output field: {field}")
        for field in missing_output
    )

    if output.get("risk_level") not in RISK_LEVELS:
        failures.append(failure(path, line_number, example_id, "invalid risk_level"))

    if output.get("referral") not in REFERRALS:
        failures.append(failure(path, line_number, example_id, "invalid referral"))

    for list_field in ("red_flags", "sus_basis"):
        if not isinstance(output.get(list_field), list):
            failures.append(failure(path, line_number, example_id, f"{list_field} must be a list"))

    limitations = output.get("limitations")
    if not isinstance(limitations, str) or "nao substitui" not in limitations.lower():
        failures.append(failure(path, line_number, example_id, "limitations must state nao substitui"))

    safety_notice = output.get("safety_notice")
    if not isinstance(safety_notice, str) or not has_escalation_notice(safety_notice):
        failures.append(failure(path, line_number, example_id, "safety_notice must include escalation guidance"))

    return failures


def failure(path: Path, line_number: int, example_id: str, reason: str) -> DatasetFailure:
    return DatasetFailure(path=path, line_number=line_number, example_id=example_id, reason=reason)


def has_escalation_notice(value: str) -> bool:
    normalized = value.lower()
    return any(term in normalized for term in ("upa", "emergencia", "samu", "atendimento"))


def format_failures(failures: list[DatasetFailure]) -> str:
    return "\n".join(
        f"- {item.path}:{item.line_number} {item.example_id}: {item.reason}" for item in failures
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate fine-tuning JSONL datasets.")
    parser.add_argument("paths", nargs="*", type=Path, default=list(DEFAULT_DATASETS))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures = [failure for path in args.paths for failure in validate_dataset(path)]
    if failures:
        print("Fine-tuning dataset validation failures:")
        print(format_failures(failures))
        return 1

    print("Fine-tuning datasets valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
