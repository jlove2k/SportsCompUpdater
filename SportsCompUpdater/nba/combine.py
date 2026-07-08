from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from nba.stats import PlayerStats


def combine_player_stats(season_rows: Iterable[dict[str, object]]) -> dict[str, PlayerStats]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    for row in season_rows:
        player = str(row["PLAYER_NAME"]).strip()
        totals[player]["points"] += float(row.get("PTS", 0) or 0)
        totals[player]["rebounds"] += float(row.get("REB", 0) or 0)
        totals[player]["assists"] += float(row.get("AST", 0) or 0)
        totals[player]["blocks"] += float(row.get("BLK", 0) or 0)
        totals[player]["steals"] += float(row.get("STL", 0) or 0)
        totals[player]["three_pm"] += float(row.get("FG3M", 0) or 0)
        totals[player]["fga"] += float(row.get("FGA", 0) or 0)
        totals[player]["fgm"] += float(row.get("FGM", 0) or 0)
        totals[player]["fta"] += float(row.get("FTA", 0) or 0)
        totals[player]["ftm"] += float(row.get("FTM", 0) or 0)

    combined: dict[str, PlayerStats] = {}
    for player, values in totals.items():
        fga = int(values["fga"])
        fgm = int(values["fgm"])
        fta = int(values["fta"])
        ftm = int(values["ftm"])
        combined[player] = PlayerStats(
            points=int(values["points"]),
            rebounds=int(values["rebounds"]),
            assists=int(values["assists"]),
            blocks=int(values["blocks"]),
            steals=int(values["steals"]),
            ft_pct=round(ftm / fta, 3) if fta else 0.0,
            fg_pct=round(fgm / fga, 3) if fga else 0.0,
            three_pm=int(values["three_pm"]),
            fga=fga,
            fgm=fgm,
            fta=fta,
            ftm=ftm,
        )
    return combined

