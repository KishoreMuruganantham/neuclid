"""SQLite memory database for experience-based learning."""

import sqlite3
import json
import time
from config import SQLITE_DB_PATH


def get_connection():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS experience_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT NOT NULL,
            parsed_json TEXT,
            problem_domain TEXT,
            retrieved_context TEXT,
            solver_code TEXT,
            final_answer TEXT,
            explanation TEXT,
            verifier_outcome TEXT,
            is_correct INTEGER DEFAULT 1,
            user_feedback TEXT,
            learned_rule TEXT,
            created_at REAL NOT NULL,
            updated_at REAL
        );

        CREATE TABLE IF NOT EXISTS ocr_corrections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_ocr TEXT NOT NULL,
            corrected_text TEXT NOT NULL,
            created_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS agent_traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            task_description TEXT,
            output TEXT,
            duration_ms REAL,
            created_at REAL NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def save_experience(
    original_text: str,
    parsed_json: str = None,
    problem_domain: str = None,
    retrieved_context: str = None,
    solver_code: str = None,
    final_answer: str = None,
    explanation: str = None,
    verifier_outcome: str = None,
    is_correct: bool = True,
    user_feedback: str = None,
    learned_rule: str = None,
) -> int:
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO experience_memory
        (original_text, parsed_json, problem_domain, retrieved_context,
         solver_code, final_answer, explanation, verifier_outcome,
         is_correct, user_feedback, learned_rule, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (original_text, parsed_json, problem_domain, retrieved_context,
         solver_code, final_answer, explanation, verifier_outcome,
         1 if is_correct else 0, user_feedback, learned_rule, time.time()),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def update_feedback(experience_id: int, is_correct: bool, feedback: str, learned_rule: str = None):
    conn = get_connection()
    conn.execute(
        """UPDATE experience_memory
        SET is_correct = ?, user_feedback = ?, learned_rule = ?, updated_at = ?
        WHERE id = ?""",
        (1 if is_correct else 0, feedback, learned_rule, time.time(), experience_id),
    )
    conn.commit()
    conn.close()


def get_recent_experiences(limit: int = 20) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM experience_memory ORDER BY created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_learned_rules() -> list[dict]:
    """Get all experiences that have learned rules (from corrections)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM experience_memory WHERE learned_rule IS NOT NULL AND learned_rule != '' ORDER BY created_at DESC",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_ocr_correction(original: str, corrected: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO ocr_corrections (original_ocr, corrected_text, created_at) VALUES (?, ?, ?)",
        (original, corrected, time.time()),
    )
    conn.commit()
    conn.close()


def get_ocr_corrections() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ocr_corrections ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_agent_trace(session_id: str, agent_name: str, task_desc: str, output: str, duration_ms: float):
    conn = get_connection()
    conn.execute(
        "INSERT INTO agent_traces (session_id, agent_name, task_description, output, duration_ms, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, agent_name, task_desc, output, duration_ms, time.time()),
    )
    conn.commit()
    conn.close()


def get_session_traces(session_id: str) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM agent_traces WHERE session_id = ? ORDER BY created_at ASC",
        (session_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


init_db()
