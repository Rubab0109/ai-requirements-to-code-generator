"""Small SQLite storage module.

This keeps the app beginner-friendly while still meeting the storage requirement.
For a production system, you can later replace this with SQLAlchemy/PostgreSQL.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import get_settings


settings = get_settings()
DB_PATH = Path(settings.SQLITE_DB_PATH)


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create required database table if it does not exist."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                requirements TEXT NOT NULL,
                generated_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def create_project(title: str, requirements: str, generated: dict[str, Any]) -> dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO projects (title, requirements, generated_json, created_at) VALUES (?, ?, ?, ?)",
            (title, requirements, json.dumps(generated, ensure_ascii=False), created_at),
        )
        conn.commit()
        project_id = int(cursor.lastrowid)
    return get_project(project_id)  # type: ignore[return-value]


def list_projects(limit: int = 25) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, title, requirements, created_at FROM projects ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "requirements_preview": (row["requirements"][:120] + "...") if len(row["requirements"]) > 120 else row["requirements"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def get_project(project_id: int) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "requirements": row["requirements"],
        "generated": json.loads(row["generated_json"]),
        "created_at": row["created_at"],
    }


def delete_project(project_id: int) -> bool:
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
    return cursor.rowcount > 0
