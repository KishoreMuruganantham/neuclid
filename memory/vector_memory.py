"""Vector-based experience memory for finding similar past problems."""

import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL, MEMORY_TOP_K
from memory.db import get_learned_rules, get_recent_experiences


def _get_memory_collection():
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    return client.get_or_create_collection(name="experience_memory", embedding_function=ef)


def store_problem_embedding(experience_id: int, problem_text: str, metadata: dict = None):
    """Store a problem's embedding in the vector memory."""
    collection = _get_memory_collection()
    meta = metadata or {}
    meta["experience_id"] = experience_id
    collection.upsert(
        ids=[f"exp_{experience_id}"],
        documents=[problem_text],
        metadatas=[meta],
    )


def search_similar_problems(query: str, top_k: int = MEMORY_TOP_K) -> list[dict]:
    """Find similar past problems from experience memory."""
    collection = _get_memory_collection()
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
    )

    similar = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            dist = results["distances"][0][i] if results["distances"] else 999
            similar.append({
                "problem_text": doc,
                "experience_id": meta.get("experience_id"),
                "distance": round(dist, 4),
                "metadata": meta,
            })
    return similar


def get_experience_warnings(problem_text: str) -> str:
    """Search for past mistakes on similar problems and format as warnings.

    This is injected directly into agent prompts to prevent repeated errors.
    """
    similar = search_similar_problems(problem_text)
    rules = get_learned_rules()

    warnings = []

    for item in similar:
        exp_id = item.get("experience_id")
        if exp_id:
            for rule in rules:
                if rule["id"] == exp_id and rule.get("learned_rule"):
                    warnings.append(
                        f"WARNING - PAST EXPERIENCE (problem similarity: {1 - item['distance']:.0%}): "
                        f"When solving a similar problem, the AI made this mistake: "
                        f"{rule.get('user_feedback', 'unknown error')}. "
                        f"LEARNED RULE: {rule['learned_rule']}"
                    )

    if not warnings and rules:
        for rule in rules[:3]:
            if rule.get("learned_rule"):
                warnings.append(
                    f"GENERAL LEARNED RULE from past correction: {rule['learned_rule']}"
                )

    return "\n\n".join(warnings) if warnings else ""
