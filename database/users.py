import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database.sqlite3"


def get_connection():
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT NOT NULL DEFAULT 'fa' CHECK(language IN ('fa', 'en')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_language(user_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    return row["language"] if row else None


def set_language(user_id: int, language: str):
    if language not in {"fa", "en"}:
        raise ValueError("Unsupported language")
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO users (user_id, language)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                language = excluded.language,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, language),
        )
