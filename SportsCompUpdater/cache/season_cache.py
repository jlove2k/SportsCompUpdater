from __future__ import annotations

from pathlib import Path
from typing import Any

from cache.sqlite import SQLiteCache


class SeasonCache:
    def __init__(self, path: Path) -> None:
        self.cache = SQLiteCache(path)

    def get_rows(self, season: str, season_type: str) -> list[dict[str, Any]] | None:
        return self.cache.get_json(self._key(season, season_type))

    def set_rows(self, season: str, season_type: str, rows: list[dict[str, Any]]) -> None:
        self.cache.set_json(self._key(season, season_type), rows)

    @staticmethod
    def _key(season: str, season_type: str) -> str:
        return f"nba_api:league_dash_player_stats:{season}:{season_type}"

