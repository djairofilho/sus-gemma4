from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from rag.scripts.ingest_documents import DocumentChunk, PROCESSED_PATH, ingest_documents, write_chunks


ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "rag" / "index" / "lexical_index.jsonl"


@dataclass(frozen=True)
class IndexedChunk:
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
    terms: dict[str, int]


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    score: int
    title: str
    section: str
    text: str
    source_url: str
    publisher: str


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZÀ-ÿ0-9]+", text.lower())


def index_chunks(chunks: list[DocumentChunk]) -> list[IndexedChunk]:
    indexed: list[IndexedChunk] = []
    for chunk in chunks:
        terms = dict(Counter(tokenize(f"{chunk.title} {chunk.section} {chunk.text}")))
        indexed.append(
            IndexedChunk(
                id=chunk.id,
                document_id=chunk.document_id,
                source_id=chunk.source_id,
                title=chunk.title,
                section=chunk.section,
                text=chunk.text,
                source_url=chunk.source_url,
                publisher=chunk.publisher,
                retrieved_at=chunk.retrieved_at,
                language=chunk.language,
                terms=terms,
            )
        )
    return indexed


def write_index(indexed_chunks: list[IndexedChunk], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(asdict(chunk), ensure_ascii=False, sort_keys=True) for chunk in indexed_chunks]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_index(path: Path) -> list[IndexedChunk]:
    chunks: list[IndexedChunk] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        chunks.append(IndexedChunk(**json.loads(line)))
    return chunks


def search(query: str, indexed_chunks: list[IndexedChunk], limit: int = 3) -> list[SearchResult]:
    query_terms = tokenize(query)
    scored: list[SearchResult] = []
    for chunk in indexed_chunks:
        score = sum(chunk.terms.get(term, 0) for term in query_terms)
        if score <= 0:
            continue
        scored.append(
            SearchResult(
                chunk_id=chunk.id,
                score=score,
                title=chunk.title,
                section=chunk.section,
                text=chunk.text,
                source_url=chunk.source_url,
                publisher=chunk.publisher,
            )
        )

    return sorted(scored, key=lambda result: (-result.score, result.chunk_id))[:limit]


def build_index(output_path: Path = INDEX_PATH) -> list[IndexedChunk]:
    chunks = ingest_documents()
    write_chunks(chunks, PROCESSED_PATH)
    indexed = index_chunks(chunks)
    write_index(indexed, output_path)
    return indexed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or search the local lexical RAG index.")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--query", type=str)
    parser.add_argument("--index", type=Path, default=INDEX_PATH)
    parser.add_argument("--limit", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.build:
        indexed = build_index(args.index)
        print(f"Indexed {len(indexed)} chunks into {args.index}")

    if args.query:
        indexed = load_index(args.index)
        for result in search(args.query, indexed, limit=args.limit):
            print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
