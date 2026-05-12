import yaml

from rag.scripts.validate_sources import (
    validate_finetuning_sources,
    validate_official_sources,
)


def write_yaml(path, payload: dict[str, object]) -> None:
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


def test_validate_official_sources_accepts_valid_registry(tmp_path) -> None:
    path = tmp_path / "official.yml"
    write_yaml(path, {"sources": [official_source()]})

    assert validate_official_sources(path) == []


def test_validate_official_sources_requires_citation(tmp_path) -> None:
    source = official_source()
    source["citation_required"] = False
    path = tmp_path / "official.yml"
    write_yaml(path, {"sources": [source]})

    failures = validate_official_sources(path)

    assert any("must require citation" in failure.reason for failure in failures)


def test_validate_official_sources_requires_https_url(tmp_path) -> None:
    source = official_source()
    source["base_url"] = "http://example.test"
    path = tmp_path / "official.yml"
    write_yaml(path, {"sources": [source]})

    failures = validate_official_sources(path)

    assert any("https URL" in failure.reason for failure in failures)


def test_validate_finetuning_sources_accepts_valid_registry(tmp_path) -> None:
    path = tmp_path / "finetuning.yml"
    write_yaml(path, {"sources": [finetuning_source()]})

    assert validate_finetuning_sources(path) == []


def test_validate_finetuning_sources_restricts_patient_data(tmp_path) -> None:
    source = finetuning_source()
    source["contains_patient_data"] = True
    source["requires_credentialing"] = False
    path = tmp_path / "finetuning.yml"
    write_yaml(path, {"sources": [source]})

    failures = validate_finetuning_sources(path)

    assert any("must require credentialing" in failure.reason for failure in failures)
