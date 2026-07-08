from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config import AppConfig
from excel.parser import PlayerRow, read_player_rows
from excel.updater import write_player_stats
from excel.workbook import load_workbook_for_update, save_workbook
from nba.provider import PlayerStatsProvider
from reports.writer import write_reports


@dataclass(frozen=True)
class UpdateResult:
    output_path: Path
    matched_count: int
    unmatched_players: list[str]
    report_json: Path
    report_csv: Path


class SportsCompEngine:
    def __init__(self, config: AppConfig, provider: PlayerStatsProvider, report_dir: Path) -> None:
        self.config = config
        self.provider = provider
        self.report_dir = report_dir

    def update_workbook(
        self,
        input_path: Path,
        output_path: Path,
        season: str,
        sheet_name: str | None = None,
    ) -> UpdateResult:
        workbook, sheet = load_workbook_for_update(input_path, sheet_name)
        player_rows = read_player_rows(
            sheet=sheet,
            player_column=self.config.player_column,
            first_data_row=self.config.first_data_row,
        )
        stats_by_name = self.provider.get_combined_stats(season=season)

        matched: list[dict[str, object]] = []
        unmatched: list[PlayerRow] = []

        for player_row in player_rows:
            match = self.provider.match_player(player_row.name, stats_by_name)
            if match is None:
                unmatched.append(player_row)
                continue

            write_player_stats(
                sheet=sheet,
                row=player_row.row_number,
                stats=match.stats,
                stat_columns=self.config.columns,
            )
            matched.append(
                {
                    "row": player_row.row_number,
                    "workbook_name": player_row.name,
                    "matched_name": match.player_name,
                    "score": match.score,
                    "stats": match.stats.to_dict(),
                }
            )

        save_workbook(workbook, output_path)
        report_json, report_csv = write_reports(
            report_dir=self.report_dir,
            matched=matched,
            unmatched=[{"row": row.row_number, "name": row.name} for row in unmatched],
        )
        return UpdateResult(
            output_path=output_path,
            matched_count=len(matched),
            unmatched_players=[row.name for row in unmatched],
            report_json=report_json,
            report_csv=report_csv,
        )

