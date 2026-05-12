import json
from pathlib import Path

from finetuning.scripts.validate_dataset import validate_dataset


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def example() -> dict[str, object]:
    return {
        "id": "example_001",
        "instruction": "Retorne JSON valido.",
        "input": "Caso sintetico.",
        "context": "",
        "output": {
            "risk_level": "low",
            "summary": "Demanda simples.",
            "suggested_action": "Orientar UBS se necessario.",
            "referral": "UBS",
            "red_flags": [],
            "sus_basis": ["Sem contexto RAG especifico recuperado."],
            "limitations": "Esta orientacao nao substitui avaliacao profissional.",
            "safety_notice": "Buscar atendimento se houver piora.",
        },
        "tags": ["schema"],
        "split": "train",
        "source": "synthetic",
    }


def test_validate_dataset_accepts_valid_example(tmp_path: Path) -> None:
    path = tmp_path / "dataset.jsonl"
    write_jsonl(path, [example()])

    assert validate_dataset(path) == []


def test_validate_dataset_requires_schema_output(tmp_path: Path) -> None:
    row = example()
    output = row["output"]
    assert isinstance(output, dict)
    output.pop("risk_level")
    path = tmp_path / "dataset.jsonl"
    write_jsonl(path, [row])

    failures = validate_dataset(path)

    assert any("missing output field: risk_level" in failure.reason for failure in failures)


def test_validate_dataset_rejects_non_synthetic_source(tmp_path: Path) -> None:
    row = example()
    row["source"] = "patient_export"
    path = tmp_path / "dataset.jsonl"
    write_jsonl(path, [row])

    failures = validate_dataset(path)

    assert any("source must be synthetic" in failure.reason for failure in failures)


def test_validate_dataset_requires_limitations(tmp_path: Path) -> None:
    row = example()
    output = row["output"]
    assert isinstance(output, dict)
    output["limitations"] = "Apenas informativo."
    path = tmp_path / "dataset.jsonl"
    write_jsonl(path, [row])

    failures = validate_dataset(path)

    assert any("limitations must state" in failure.reason for failure in failures)
