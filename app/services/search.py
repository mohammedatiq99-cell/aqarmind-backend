from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from app.core.config import get_settings


def search_is_configured() -> bool:
    s = get_settings()
    return all([s.azure_search_endpoint, s.azure_search_api_key, s.azure_search_index])


def retrieve_knowledge(question: str, top_k: int = 5) -> list[dict]:
    s = get_settings()
    if not search_is_configured():
        raise RuntimeError("Azure AI Search configuration is incomplete.")

    client = SearchClient(
        endpoint=s.azure_search_endpoint,
        index_name=s.azure_search_index,
        credential=AzureKeyCredential(s.azure_search_api_key),
    )

    kwargs = {
        "search_text": question,
        "top": top_k,
        "select": ["chunk_id", "title", "chunk", "content_url", "source", "doc_type"],
    }

    # Semantic configuration is optional in this public reference implementation.
    if s.azure_search_semantic_config:
        kwargs.update(
            {
                "query_type": "semantic",
                "semantic_configuration_name": s.azure_search_semantic_config,
            }
        )

    results = client.search(**kwargs)
    return [
        {
            "chunk_id": item.get("chunk_id"),
            "title": item.get("title"),
            "content": item.get("chunk"),
            "source_url": item.get("content_url"),
            "source": item.get("source"),
            "doc_type": item.get("doc_type"),
            "score": item.get("@search.score"),
        }
        for item in results
    ]
