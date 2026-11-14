import sqlite3
from datetime import datetime

from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dictionaries
    return conn


def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id          TEXT PRIMARY KEY,
                filename    TEXT NOT NULL,
                file_type   TEXT NOT NULL,
                domain      TEXT NOT NULL,
                num_chunks  INTEGER NOT NULL,
                uploaded_at TEXT NOT NULL
            )
        """)


def add_document(doc_id, filename, file_type, domain, num_chunks):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?)",
            (doc_id, filename, file_type, domain, num_chunks,
             datetime.now().isoformat(timespec="seconds")),
        )


def list_documents():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM documents ORDER BY uploaded_at DESC").fetchall()
    return [dict(row) for row in rows]


def list_domains():
    with get_connection() as conn:
        rows = conn.execute("SELECT DISTINCT domain FROM documents ORDER BY domain").fetchall()
    return [row["domain"] for row in rows]


create_tables()
