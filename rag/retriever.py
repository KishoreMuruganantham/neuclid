"""Retrieve relevant math knowledge from ChromaDB."""

from rag.embeddings import build_vector_store, get_or_create_collection
from config import RAG_TOP_K


def retrieve_context(query: str, top_k: int = RAG_TOP_K) -> list[dict]:
    """Query the vector store and return relevant chunks with metadata.

    Returns list of dicts: [{"text": ..., "source": ..., "topic": ..., "distance": ...}]
    """
    collection = build_vector_store()

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
    )

    retrieved = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            dist = results["distances"][0][i] if results["distances"] else 0
            retrieved.append({
                "text": doc,
                "source": meta.get("source", "unknown"),
                "topic": meta.get("topic", "unknown"),
                "distance": round(dist, 4),
            })

    return retrieved


def format_context_for_prompt(retrieved: list[dict]) -> str:
    """Format retrieved chunks into a prompt-friendly string."""
    if not retrieved:
        return "No relevant knowledge base context found."

    parts = ["## Retrieved Mathematical Context\n"]
    for i, item in enumerate(retrieved, 1):
        parts.append(
            f"### Source {i}: {item['topic']} ({item['source']})\n{item['text']}\n"
        )
    return "\n".join(parts)
