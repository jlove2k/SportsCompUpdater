from __future__ import annotations

from pathlib import Path
from typing import Protocol

from cache.season_cache import SeasonCache
from nba.combine import combine_player_stats
from nba.matcher import PlayerMatch, match_player_name
from nba.stats import PlayerStats


class PlayerStatsProvider(Protocol):
    def get_combined_stats(self, season: str) -> dict[str, PlayerStats]:
        ...

    def match_player(self, player_name: str, stats_by_player: dict[str, PlayerStats]) -> PlayerMatch | None:
        ...


class NbaApiStatsProvider:
    def __init__(self, cache_path: Path, min_match_score: int = 88) -> None:
        self.cache = SeasonCache(cache_path)
        self.min_match_score = min_match_score

    def get_combined_stats(self, season: str) -> dict[str, PlayerStats]:
        rows = []
        rows.extend(self._load_rows(season, "Regular Season"))
        rows.extend(self._load_rows(season, "Playoffs"))
        return combine_player_stats(rows)

    def match_player(self, player_name: str, stats_by_player: dict[str, PlayerStats]) -> PlayerMatch | None:
        return match_player_name(player_name, stats_by_player, min_score=self.min_match_score)

    def _load_rows(self, season: str, season_type: str) -> list[dict[str, object]]:
        cached = self.cache.get_rows(season, season_type)
        if cached is not None:
            return cached

        from nba_api.stats.endpoints import leaguedashplayerstats

        endpoint = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star=season_type,
            per_mode_detailed="Totals",
            timeout=60,
        )
        frame = endpoint.get_data_frames()[0]
        rows = frame.to_dict(orient="records")
        self.cache.set_rows(season, season_type, rows)
        return rows

