import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "groq/llama-3.3-70b-versatile")
GEMINI_VISION_MODEL = os.getenv("GEMINI_VISION_MODEL", "gemini-2.5-flash")

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
