from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class SQLiteCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache_items (
                    cache_key TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def get_json(self, key: str) -> Any | None:
        with sqlite3.connect(self.path) as conn:
            row = conn.execute("SELECT payload FROM cache_items WHERE cache_key = ?", (key,)).fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def set_json(self, key: str, payload: Any) -> None:
        text = json.dumps(payload)
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO cache_items(cache_key, payload)
                VALUES (?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    payload = excluded.payload,
                    created_at = CURRENT_TIMESTAMP
                """,
                (key, text),
            )

