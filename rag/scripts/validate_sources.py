from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
OFFICIAL_SOURCES_PATH = ROOT / "data" / "sources" / "official_sources.yml"
FINETUNING_SOURCES_PATH = ROOT / "data" / "sources" / "finetuning_sources.yml"
DOCUMENT_MANIFEST_PATH = ROOT / "rag" / "documents" / "manifest.yml"

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

DOCUMENT_REQUIRED_FIELDS = {
    "id",
    "source_id",
    "title",
    "source_url",
    "publisher",
    "retrieved_at",
    "license",
    "language",
    "local_path",
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
            failures.append(
                SourceValidationFailure(source_id, "official RAG source must require citation")
            )

        if source.get("access") not in {"public", "restricted"}:
            failures.append(
                SourceValidationFailure(source_id, "access must be public or restricted")
            )

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


def validate_document_manifest(
    manifest_path: Path,
    official_sources_path: Path = OFFICIAL_SOURCES_PATH,
    root: Path = ROOT,
) -> list[SourceValidationFailure]:
    payload = load_yaml(manifest_path)
    documents = payload.get("documents")
    if not isinstance(documents, list):
        return [SourceValidationFailure(str(manifest_path), "missing documents list")]

    official_source_ids = load_source_ids(official_sources_path)
    failures: list[SourceValidationFailure] = []
    seen_ids: set[str] = set()

    for document in documents:
        failures.extend(validate_mapping(document, DOCUMENT_REQUIRED_FIELDS))
        if not isinstance(document, dict):
            continue

        document_id = str(document.get("id", "unknown"))
        failures.extend(validate_unique_id(document_id, seen_ids))
        failures.extend(validate_url(document_id, document.get("source_url")))

        source_id = document.get("source_id")
        if not isinstance(source_id, str) or source_id not in official_source_ids:
            failures.append(
                SourceValidationFailure(document_id, "source_id must reference an official source")
            )

        if document.get("language") != "pt-BR":
            failures.append(SourceValidationFailure(document_id, "language must be pt-BR"))

        local_path = document.get("local_path")
        if not isinstance(local_path, str):
            failures.append(SourceValidationFailure(document_id, "local_path must be a string"))
        else:
            failures.extend(validate_local_document_path(document_id, root / local_path, root))

        for required_text_field in ("title", "publisher", "retrieved_at", "license", "notes"):
            value = document.get(required_text_field)
            if not isinstance(value, str) or not value.strip():
                failures.append(
                    SourceValidationFailure(document_id, f"{required_text_field} must be non-empty")
                )

    return failures


def load_source_ids(path: Path) -> set[str]:
    payload = load_yaml(path)
    sources = payload.get("sources")
    if not isinstance(sources, list):
        return set()

    return {
        source["id"]
        for source in sources
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }


def validate_local_document_path(
    document_id: str,
    document_path: Path,
    root: Path,
) -> list[SourceValidationFailure]:
    try:
        document_path.relative_to(root / "rag" / "documents" / "raw")
    except ValueError:
        return [SourceValidationFailure(document_id, "local_path must be under rag/documents/raw")]

    if document_path.suffix.lower() not in {".md", ".txt"}:
        return [SourceValidationFailure(document_id, "local_path must point to .md or .txt")]

    if not document_path.exists():
        return [SourceValidationFailure(document_id, "local_path does not exist")]

    return []


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
    parser.add_argument("--manifest", type=Path, default=DOCUMENT_MANIFEST_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures = [
        *validate_official_sources(args.official),
        *validate_finetuning_sources(args.finetuning),
        *validate_document_manifest(args.manifest, official_sources_path=args.official),
    ]

    if failures:
        print("Source validation failures:")
        print(format_failures(failures))
        return 1

    print("Source registries valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
