from app.agent.rag import LocalMarkdownRag


def test_local_rag_returns_simulated_sources() -> None:
    rag = LocalMarkdownRag()
    results = rag.search("desempleo documentos subsidio")

    assert results
    assert any("desempleo" in result.title.lower() for result in results)
