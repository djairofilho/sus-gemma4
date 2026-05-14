from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from rag.scripts.ingest_documents import (
    PROCESSED_PATH,
    DocumentChunk,
    ingest_documents,
    write_chunks,
)

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "rag" / "index" / "lexical_index.jsonl"
STOPWORDS = {
    "a",
    "ao",
    "aos",
    "as",
    "com",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "na",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "ou",
    "para",
    "por",
}


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
    vector: dict[str, float]


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    score: int
    title: str
    section: str
    text: str
    source_url: str
    publisher: str


def normalize_for_search(text: str) -> str:
    without_accents = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return without_accents.lower()


def tokenize(text: str, *, remove_stopwords: bool = False) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9]+", normalize_for_search(text))
    if remove_stopwords:
        return [token for token in tokens if token not in STOPWORDS]
    return tokens


def index_chunks(chunks: list[DocumentChunk]) -> list[IndexedChunk]:
    indexed: list[IndexedChunk] = []
    for chunk in chunks:
        terms = weighted_terms(chunk)
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
                vector=normalize_vector(terms),
            )
        )
    return indexed


def weighted_terms(chunk: DocumentChunk) -> dict[str, int]:
    terms: Counter[str] = Counter()
    terms.update({term: count * 3 for term, count in Counter(tokenize(chunk.title)).items()})
    terms.update({term: count * 2 for term, count in Counter(tokenize(chunk.section)).items()})
    terms.update(Counter(tokenize(chunk.text)))
    return dict(terms)


def normalize_vector(terms: dict[str, int]) -> dict[str, float]:
    magnitude = math.sqrt(sum(weight * weight for weight in terms.values()))
    if magnitude == 0:
        return {}
    return {term: weight / magnitude for term, weight in terms.items()}


def write_index(indexed_chunks: list[IndexedChunk], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps(asdict(chunk), ensure_ascii=False, sort_keys=True)
        for chunk in indexed_chunks
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_index(path: Path) -> list[IndexedChunk]:
    chunks: list[IndexedChunk] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if "vector" not in payload:
            payload["vector"] = normalize_vector(payload["terms"])
        chunks.append(IndexedChunk(**payload))
    return chunks


def search(query: str, indexed_chunks: list[IndexedChunk], limit: int = 3) -> list[SearchResult]:
    query_terms = tokenize(query, remove_stopwords=True)
    if not query_terms:
        return []

    normalized_query = " ".join(query_terms)
    query_vector = normalize_vector(dict(Counter(query_terms)))
    scored: list[SearchResult] = []
    for chunk in indexed_chunks:
        score = hybrid_score(query_terms, query_vector, normalized_query, chunk)
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


def hybrid_score(
    query_terms: list[str],
    query_vector: dict[str, float],
    normalized_query: str,
    chunk: IndexedChunk,
) -> int:
    lexical_score = sum(chunk.terms.get(term, 0) for term in query_terms)
    vector_score = cosine_similarity(query_vector, chunk.vector)
    return lexical_score + int(round(vector_score * 10)) + phrase_bonus(normalized_query, chunk)


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    return sum(weight * right.get(term, 0.0) for term, weight in left.items())


def phrase_bonus(normalized_query: str, chunk: IndexedChunk) -> int:
    if " " not in normalized_query:
        return 0

    searchable_text = " ".join(
        tokenize(f"{chunk.title} {chunk.section} {chunk.text}", remove_stopwords=True)
    )
    if normalized_query not in searchable_text:
        return 0

    return len(normalized_query.split()) * 3


def build_index(output_path: Path = INDEX_PATH) -> list[IndexedChunk]:
    chunks = ingest_documents()
    write_chunks(chunks, PROCESSED_PATH)
    indexed = index_chunks(chunks)
    write_index(indexed, output_path)
    return indexed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or search the local hybrid RAG index.")
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
