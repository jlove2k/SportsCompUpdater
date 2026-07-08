from __future__ import annotations

from openpyxl.worksheet.worksheet import Worksheet

from nba.stats import PlayerStats


def write_player_stats(sheet: Worksheet, row: int, stats: PlayerStats, stat_columns: dict[str, str]) -> None:
    values = stats.to_dict()
    for stat_name, column in stat_columns.items():
        sheet[f"{column}{row}"].value = values[stat_name]

