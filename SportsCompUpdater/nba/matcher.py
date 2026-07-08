from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher

from nba.normalize import normalize_name
from nba.stats import PlayerStats


@dataclass(frozen=True)
class PlayerMatch:
    player_name: str
    score: int
    stats: PlayerStats


def match_player_name(
    query_name: str,
    stats_by_player: dict[str, PlayerStats],
    min_score: int = 88,
) -> PlayerMatch | None:
    normalized_lookup = {normalize_name(name): name for name in stats_by_player}
    normalized_query = normalize_name(query_name)

    if normalized_query in normalized_lookup:
        player_name = normalized_lookup[normalized_query]
        return PlayerMatch(player_name=player_name, score=100, stats=stats_by_player[player_name])

    best_normalized_name, score = _best_name_match(normalized_query, normalized_lookup.keys())
    if best_normalized_name is None:
        return None

    if score < min_score:
        return None

    player_name = normalized_lookup[best_normalized_name]
    return PlayerMatch(player_name=player_name, score=int(score), stats=stats_by_player[player_name])


def _best_name_match(query: str, choices: object) -> tuple[str | None, int]:
    try:
        from rapidfuzz import fuzz, process

        best = process.extractOne(query, choices, scorer=fuzz.WRatio)
        if best is None:
            return None, 0
        name, score, _ = best
        return str(name), int(score)
    except ModuleNotFoundError:
        best_name: str | None = None
        best_score = 0
        for choice in choices:
            candidate = str(choice)
            score = int(SequenceMatcher(None, query, candidate).ratio() * 100)
            if score > best_score:
                best_name = candidate
                best_score = score
        return best_name, best_score
