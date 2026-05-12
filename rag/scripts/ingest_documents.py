from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "rag" / "documents" / "manifest.yml"
PROCESSED_PATH = ROOT / "rag" / "documents" / "processed" / "chunks.jsonl"


@dataclass(frozen=True)
class DocumentManifestEntry:
    id: str
    source_id: str
    title: str
    source_url: str
    publisher: str
    retrieved_at: str
    license: str
    language: str
    local_path: str
    notes: str


@dataclass(frozen=True)
class DocumentChunk:
    id: str
    document_id: str
    source_id: str
    title: str
    section: str
    text: str
    source_url: str
    publisher: str
    retrieved_at: str
    language: str


def load_manifest(path: Path) -> list[DocumentManifestEntry]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("documents"), list):
        raise ValueError("manifest must contain a documents list")

    return [DocumentManifestEntry(**entry) for entry in payload["documents"]]


def read_document(entry: DocumentManifestEntry, root: Path = ROOT) -> str:
    document_path = root / entry.local_path
    if document_path.suffix.lower() not in {".md", ".txt"}:
        raise ValueError(f"unsupported document type: {document_path.suffix}")
    return document_path.read_text(encoding="utf-8")


def chunk_document(entry: DocumentManifestEntry, text: str) -> list[DocumentChunk]:
    sections = split_markdown_sections(text)
    chunks: list[DocumentChunk] = []

    for index, section in enumerate(sections, start=1):
        section_title = section["section"]
        section_text = normalize_text(section["text"])
        if not section_text:
            continue

        chunks.append(
            DocumentChunk(
                id=f"{entry.id}::chunk_{index:04d}",
                document_id=entry.id,
                source_id=entry.source_id,
                title=entry.title,
                section=section_title,
                text=section_text,
                source_url=entry.source_url,
                publisher=entry.publisher,
                retrieved_at=entry.retrieved_at,
                language=entry.language,
            )
        )

    return chunks


def split_markdown_sections(text: str) -> list[dict[str, str]]:
    current_section = "Document"
    current_lines: list[str] = []
    sections: list[dict[str, str]] = []

    for line in text.splitlines():
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            if current_lines:
                sections.append({"section": current_section, "text": "\n".join(current_lines)})
                current_lines = []
            current_section = heading_match.group(2).strip()
            continue

        current_lines.append(line)

    if current_lines:
        sections.append({"section": current_section, "text": "\n".join(current_lines)})

    return sections


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def ingest_documents(manifest_path: Path = MANIFEST_PATH, root: Path = ROOT) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for entry in load_manifest(manifest_path):
        chunks.extend(chunk_document(entry, read_document(entry, root=root)))
    return chunks


def write_chunks(chunks: list[DocumentChunk], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(asdict(chunk), ensure_ascii=False, sort_keys=True) for chunk in chunks]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest local RAG documents into chunks.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=PROCESSED_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    chunks = ingest_documents(args.manifest)
    write_chunks(chunks, args.output)
    print(f"Ingested {len(chunks)} chunks into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
