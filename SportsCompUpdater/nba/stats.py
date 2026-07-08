from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerStats:
    points: int = 0
    rebounds: int = 0
    assists: int = 0
    blocks: int = 0
    steals: int = 0
    ft_pct: float = 0.0
    fg_pct: float = 0.0
    three_pm: int = 0
    fga: int = 0
    fgm: int = 0
    fta: int = 0
    ftm: int = 0

    def to_dict(self) -> dict[str, int | float]:
        return {
            "points": self.points,
            "rebounds": self.rebounds,
            "assists": self.assists,
            "blocks": self.blocks,
            "steals": self.steals,
            "ft_pct": self.ft_pct,
            "fg_pct": self.fg_pct,
            "three_pm": self.three_pm,
            "fga": self.fga,
            "fgm": self.fgm,
            "fta": self.fta,
            "ftm": self.ftm,
        }

