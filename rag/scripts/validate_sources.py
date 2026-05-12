from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
OFFICIAL_SOURCES_PATH = ROOT / "data" / "sources" / "official_sources.yml"
FINETUNING_SOURCES_PATH = ROOT / "data" / "sources" / "finetuning_sources.yml"

OFFICIAL_REQUIRED_FIELDS = {
    "id",
    "name",
    "category",
    "publisher",
    "base_url",
    "scope",
    "use",
    "access",
    "citation_required",
    "notes",
}

FINETUNING_REQUIRED_FIELDS = {
    "id",
    "name",
    "language",
    "size",
    "use",
    "access",
    "contains_patient_data",
    "requires_credentialing",
    "notes",
}


@dataclass(frozen=True)
class SourceValidationFailure:
    source_id: str
    reason: str


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return payload


def validate_official_sources(path: Path) -> list[SourceValidationFailure]:
    payload = load_yaml(path)
    sources = payload.get("sources")
    if not isinstance(sources, list):
        return [SourceValidationFailure(str(path), "missing sources list")]

    failures: list[SourceValidationFailure] = []
    seen_ids: set[str] = set()
    for source in sources:
        failures.extend(validate_mapping(source, OFFICIAL_REQUIRED_FIELDS))
        if not isinstance(source, dict):
            continue

        source_id = str(source.get("id", "unknown"))
        failures.extend(validate_unique_id(source_id, seen_ids))
        failures.extend(validate_url(source_id, source.get("base_url")))

        if source.get("citation_required") is not True:
            failures.append(SourceValidationFailure(source_id, "official RAG source must require citation"))

        if source.get("access") not in {"public", "restricted"}:
            failures.append(SourceValidationFailure(source_id, "access must be public or restricted"))

    return failures


def validate_finetuning_sources(path: Path) -> list[SourceValidationFailure]:
    payload = load_yaml(path)
    sources = payload.get("sources")
    if not isinstance(sources, list):
        return [SourceValidationFailure(str(path), "missing sources list")]

    failures: list[SourceValidationFailure] = []
    seen_ids: set[str] = set()
    for source in sources:
        failures.extend(validate_mapping(source, FINETUNING_REQUIRED_FIELDS))
        if not isinstance(source, dict):
            continue

        source_id = str(source.get("id", "unknown"))
        failures.extend(validate_unique_id(source_id, seen_ids))

        contains_patient_data = source.get("contains_patient_data") is True
        requires_credentialing = source.get("requires_credentialing") is True
        if contains_patient_data and not requires_credentialing:
            failures.append(
                SourceValidationFailure(
                    source_id,
                    "patient-data sources must require credentialing",
                )
            )

        if source.get("language") != "pt-BR":
            failures.append(SourceValidationFailure(source_id, "language must be pt-BR"))

    return failures


def validate_mapping(source: object, required_fields: set[str]) -> list[SourceValidationFailure]:
    if not isinstance(source, dict):
        return [SourceValidationFailure("unknown", "source entry must be a mapping")]

    source_id = str(source.get("id", "unknown"))
    missing = sorted(field for field in required_fields if field not in source)
    return [SourceValidationFailure(source_id, f"missing field: {field}") for field in missing]


def validate_unique_id(source_id: str, seen_ids: set[str]) -> list[SourceValidationFailure]:
    if source_id in seen_ids:
        return [SourceValidationFailure(source_id, "duplicate source id")]

    seen_ids.add(source_id)
    return []


def validate_url(source_id: str, value: object) -> list[SourceValidationFailure]:
    if not isinstance(value, str) or not value.startswith("https://"):
        return [SourceValidationFailure(source_id, "base_url must be an https URL")]
    return []


def format_failures(failures: list[SourceValidationFailure]) -> str:
    return "\n".join(f"- {failure.source_id}: {failure.reason}" for failure in failures)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate RAG and fine-tuning source registries.")
    parser.add_argument("--official", type=Path, default=OFFICIAL_SOURCES_PATH)
    parser.add_argument("--finetuning", type=Path, default=FINETUNING_SOURCES_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures = [
        *validate_official_sources(args.official),
        *validate_finetuning_sources(args.finetuning),
    ]

    if failures:
        print("Source validation failures:")
        print(format_failures(failures))
        return 1

    print("Source registries valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
