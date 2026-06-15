from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnowledgeDocument:
    path: str
    title: str
    content: str


@dataclass(frozen=True)
class SearchResult:
    title: str
    source: str
    snippet: str
    score: int


class LocalMarkdownRag:
    def __init__(self, kb_path: str = "data/kb") -> None:
        self.kb_path = Path(kb_path)
        self.documents = self._load_documents()

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_terms = _normalize_terms(query)
        scored: list[SearchResult] = []
        for doc in self.documents:
            doc_terms = _normalize_terms(doc.content)
            score = len(query_terms.intersection(doc_terms))
            if score:
                scored.append(
                    SearchResult(
                        title=doc.title,
                        source=doc.path,
                        snippet=_best_snippet(doc.content, query_terms),
                        score=score,
                    )
                )
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]

    def _load_documents(self) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        if not self.kb_path.exists():
            return documents
        for path in sorted(self.kb_path.glob("*.md")):
            content = path.read_text(encoding="utf-8")
            title = next(
                (
                    line.lstrip("# ").strip()
                    for line in content.splitlines()
                    if line.startswith("#")
                ),
                path.stem,
            )
            documents.append(KnowledgeDocument(path=str(path), title=title, content=content))
        return documents


class AzureAiSearchRagAdapter:
    """Boundary for a future Azure AI Search implementation.

    A production implementation would authenticate with managed identity or a
    secretless connection, query AZURE_AI_SEARCH_INDEX, and return SearchResult
    objects with citations. It is intentionally not implemented here to keep the
    prototype runnable without Azure credentials.
    """

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        raise NotImplementedError("Configure Azure AI Search before using the cloud RAG adapter.")


def _normalize_terms(text: str) -> set[str]:
    cleaned = "".join(char.lower() if char.isalnum() else " " for char in text)
    return {word for word in cleaned.split() if len(word) > 3}


def _best_snippet(content: str, query_terms: set[str]) -> str:
    paragraphs = [paragraph.strip() for paragraph in content.split("\n\n") if paragraph.strip()]
    if not paragraphs:
        return ""
    ranked = sorted(
        paragraphs,
        key=lambda paragraph: len(_normalize_terms(paragraph).intersection(query_terms)),
        reverse=True,
    )
    return ranked[0][:500]
