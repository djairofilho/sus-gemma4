import sys
from pathlib import Path

from app.schemas import RagSearchResult

ROOT = Path(__file__).resolve().parents[4]
INDEX_PATH = ROOT / "rag" / "index" / "lexical_index.jsonl"
ROOT_STRING = str(ROOT)

if ROOT_STRING not in sys.path:
    sys.path.insert(0, ROOT_STRING)


def search_rag(query: str, limit: int = 3) -> list[RagSearchResult]:
    ensure_index()

    from rag.scripts.search_index import load_index, search  # type: ignore[import-not-found]

    results = search(query, load_index(INDEX_PATH), limit=limit)
    return [RagSearchResult(**result.__dict__) for result in results]


def ensure_index() -> None:
    if INDEX_PATH.exists():
        return

    from rag.scripts.search_index import build_index

    build_index(INDEX_PATH)


def rag_index_status() -> str:
    return "ready" if INDEX_PATH.exists() else "not_built"
