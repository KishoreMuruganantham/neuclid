import os
from dotenv import load_dotenv

load_dotenv()

def _get_secret(key: str, default: str = "") -> str:
    """Get secret from env vars or Streamlit secrets (for Streamlit Cloud)."""
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default

GOOGLE_API_KEY = _get_secret("GOOGLE_API_KEY")
GROQ_API_KEY = _get_secret("GROQ_API_KEY")
LLM_MODEL = _get_secret("LLM_MODEL", "groq/llama-3.3-70b-versatile")
GEMINI_VISION_MODEL = _get_secret("GEMINI_VISION_MODEL", "gemini-2.5-flash")

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "rag", "knowledge_base")
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "neuclid_memory.db")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RAG_TOP_K = 5
MEMORY_TOP_K = 3

MATH_DOMAINS = [
    "Algebra",
    "Probability",
    "Calculus - Limits",
    "Calculus - Derivatives",
    "Calculus - Optimization",
    "Linear Algebra",
]
