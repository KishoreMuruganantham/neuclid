"""Build and manage the ChromaDB vector store from knowledge base documents."""

import os
import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_PERSIST_DIR, KNOWLEDGE_BASE_DIR, EMBEDDING_MODEL


def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)


def get_or_create_collection(name: str = "math_knowledge"):
    client = get_chroma_client()
    ef = get_embedding_function()
    return client.get_or_create_collection(name=name, embedding_function=ef)


def chunk_document(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks by character count, respecting paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            words = current_chunk.split()
            overlap_text = " ".join(words[-overlap // 5 :]) if len(words) > overlap // 5 else ""
            current_chunk = overlap_text + "\n\n" + para
        else:
            current_chunk += ("\n\n" if current_chunk else "") + para

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def build_vector_store():
    """Read all knowledge base docs, chunk them, and store in ChromaDB."""
    collection = get_or_create_collection()

    existing = collection.count()
    if existing > 0:
        return collection

    all_ids = []
    all_docs = []
    all_metadata = []
    doc_id = 0

    for filename in sorted(os.listdir(KNOWLEDGE_BASE_DIR)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        topic = filename.replace(".md", "").replace("_", " ").title()
        chunks = chunk_document(content)

        for i, chunk in enumerate(chunks):
            all_ids.append(f"doc_{doc_id}")
            all_docs.append(chunk)
            all_metadata.append({
                "source": filename,
                "topic": topic,
                "chunk_index": i,
            })
            doc_id += 1

    if all_docs:
        collection.add(
            ids=all_ids,
            documents=all_docs,
            metadatas=all_metadata,
        )

    return collection


if __name__ == "__main__":
    coll = build_vector_store()
    print(f"Vector store built with {coll.count()} chunks.")
