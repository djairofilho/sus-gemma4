import importlib
import sys
from pathlib import Path
from typing import Protocol, cast

from app.schemas import RagSearchResult

ROOT = Path(__file__).resolve().parents[4]
INDEX_PATH = ROOT / "rag" / "index" / "lexical_index.jsonl"
ROOT_STRING = str(ROOT)

if ROOT_STRING not in sys.path:
    sys.path.insert(0, ROOT_STRING)


class SearchResultLike(Protocol):
    chunk_id: str
    score: int
    title: str
    section: str
    text: str
    source_url: str
    publisher: str


class SearchIndexModule(Protocol):
    def load_index(self, path: Path) -> list[object]: ...

    def search(
        self,
        query: str,
        indexed_chunks: list[object],
        limit: int = 3,
    ) -> list[SearchResultLike]: ...

    def build_index(self, output_path: Path) -> list[object]: ...


def search_rag(query: str, limit: int = 3) -> list[RagSearchResult]:
    ensure_index()

    search_index = load_search_index_module()
    results = search_index.search(query, search_index.load_index(INDEX_PATH), limit=limit)
    return [
        RagSearchResult(
            chunk_id=result.chunk_id,
            score=result.score,
            title=result.title,
            section=result.section,
            text=result.text,
            source_url=result.source_url,
            publisher=result.publisher,
        )
        for result in results
    ]


def ensure_index() -> None:
    if INDEX_PATH.exists():
        return

    search_index = load_search_index_module()

    search_index.build_index(INDEX_PATH)


def rag_index_status() -> str:
    return "ready" if INDEX_PATH.exists() else "not_built"


def load_search_index_module() -> SearchIndexModule:
    return cast(SearchIndexModule, importlib.import_module("rag.scripts.search_index"))
