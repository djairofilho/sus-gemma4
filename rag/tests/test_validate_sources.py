from pathlib import Path

import yaml
from rag.scripts.validate_sources import (
    validate_document_manifest,
    validate_finetuning_sources,
    validate_official_sources,
)


def write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def official_source() -> dict[str, object]:
    return {
        "id": "pcdt",
        "name": "PCDT",
        "category": "clinical_guidelines",
        "publisher": "Ministerio da Saude",
        "base_url": "https://www.gov.br/saude",
        "scope": "federal",
        "use": "rag",
        "access": "public",
        "citation_required": True,
        "notes": "Fonte oficial.",
    }


def finetuning_source() -> dict[str, object]:
    return {
        "id": "medpt",
        "name": "MedPT",
        "language": "pt-BR",
        "size": "384095 QA pairs",
        "use": "sft_behavior_and_language",
        "access": "public_or_research",
        "contains_patient_data": False,
        "requires_credentialing": False,
        "notes": "Fonte candidata.",
    }


def document_entry(local_path: str = "rag/documents/raw/doc.md") -> dict[str, object]:
    return {
        "id": "doc_1",
        "source_id": "pcdt",
        "title": "Documento oficial curado",
        "source_url": "https://www.gov.br/saude/doc",
        "publisher": "Ministerio da Saude",
        "retrieved_at": "2026-05-12",
        "license": "public_source_extract",
        "language": "pt-BR",
        "local_path": local_path,
        "notes": "Extrato curado para RAG.",
    }


def test_validate_official_sources_accepts_valid_registry(tmp_path: Path) -> None:
    path = tmp_path / "official.yml"
    write_yaml(path, {"sources": [official_source()]})

    assert validate_official_sources(path) == []


def test_validate_official_sources_requires_citation(tmp_path: Path) -> None:
    source = official_source()
    source["citation_required"] = False
    path = tmp_path / "official.yml"
    write_yaml(path, {"sources": [source]})

    failures = validate_official_sources(path)

    assert any("must require citation" in failure.reason for failure in failures)


def test_validate_official_sources_requires_https_url(tmp_path: Path) -> None:
    source = official_source()
    source["base_url"] = "http://example.test"
    path = tmp_path / "official.yml"
    write_yaml(path, {"sources": [source]})

    failures = validate_official_sources(path)

    assert any("https URL" in failure.reason for failure in failures)


def test_validate_finetuning_sources_accepts_valid_registry(tmp_path: Path) -> None:
    path = tmp_path / "finetuning.yml"
    write_yaml(path, {"sources": [finetuning_source()]})

    assert validate_finetuning_sources(path) == []


def test_validate_finetuning_sources_restricts_patient_data(tmp_path: Path) -> None:
    source = finetuning_source()
    source["contains_patient_data"] = True
    source["requires_credentialing"] = False
    path = tmp_path / "finetuning.yml"
    write_yaml(path, {"sources": [source]})

    failures = validate_finetuning_sources(path)

    assert any("must require credentialing" in failure.reason for failure in failures)


def test_validate_document_manifest_accepts_valid_document(tmp_path: Path) -> None:
    official_path = tmp_path / "official.yml"
    manifest_path = tmp_path / "manifest.yml"
    document_path = tmp_path / "rag" / "documents" / "raw" / "doc.md"
    document_path.parent.mkdir(parents=True)
    document_path.write_text("# Documento\n\nConteudo oficial curado.", encoding="utf-8")

    write_yaml(official_path, {"sources": [official_source()]})
    write_yaml(manifest_path, {"documents": [document_entry()]})

    assert validate_document_manifest(manifest_path, official_path, root=tmp_path) == []


def test_validate_document_manifest_requires_registered_source(tmp_path: Path) -> None:
    official_path = tmp_path / "official.yml"
    manifest_path = tmp_path / "manifest.yml"
    document_path = tmp_path / "rag" / "documents" / "raw" / "doc.md"
    document_path.parent.mkdir(parents=True)
    document_path.write_text("# Documento", encoding="utf-8")

    document = document_entry()
    document["source_id"] = "unknown_source"
    write_yaml(official_path, {"sources": [official_source()]})
    write_yaml(manifest_path, {"documents": [document]})

    failures = validate_document_manifest(manifest_path, official_path, root=tmp_path)

    assert any("source_id must reference" in failure.reason for failure in failures)


def test_validate_document_manifest_rejects_missing_local_file(tmp_path: Path) -> None:
    official_path = tmp_path / "official.yml"
    manifest_path = tmp_path / "manifest.yml"
    write_yaml(official_path, {"sources": [official_source()]})
    write_yaml(manifest_path, {"documents": [document_entry()]})

    failures = validate_document_manifest(manifest_path, official_path, root=tmp_path)

    assert any("local_path does not exist" in failure.reason for failure in failures)


def test_validate_document_manifest_rejects_paths_outside_raw(tmp_path: Path) -> None:
    official_path = tmp_path / "official.yml"
    manifest_path = tmp_path / "manifest.yml"
    document_path = tmp_path / "data" / "doc.md"
    document_path.parent.mkdir(parents=True)
    document_path.write_text("# Documento", encoding="utf-8")

    write_yaml(official_path, {"sources": [official_source()]})
    write_yaml(manifest_path, {"documents": [document_entry("data/doc.md")]})

    failures = validate_document_manifest(manifest_path, official_path, root=tmp_path)

    assert any("under rag/documents/raw" in failure.reason for failure in failures)
