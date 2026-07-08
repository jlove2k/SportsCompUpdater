from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


DEFAULT_STAT_COLUMNS = {
    "points": "E",
    "rebounds": "F",
    "assists": "G",
    "blocks": "H",
    "steals": "I",
    "ft_pct": "J",
    "fg_pct": "K",
    "three_pm": "L",
    "fga": "M",
    "fgm": "N",
    "fta": "O",
    "ftm": "P",
}


@dataclass(frozen=True)
class AppConfig:
    player_column: str = "A"
    first_data_row: int = 2
    stat_columns: dict[str, str] | None = None

    @property
    def columns(self) -> dict[str, str]:
        return self.stat_columns or DEFAULT_STAT_COLUMNS


def load_config(path: str | Path | None = None) -> AppConfig:
    if path is None:
        default_path = Path("config.json")
        if not default_path.exists():
            return AppConfig(stat_columns=DEFAULT_STAT_COLUMNS)
        path = default_path

    data: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return AppConfig(
        player_column=data.get("player_column", "A"),
        first_data_row=int(data.get("first_data_row", 2)),
        stat_columns=data.get("stat_columns", DEFAULT_STAT_COLUMNS),
    )

