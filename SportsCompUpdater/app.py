from __future__ import annotations

import argparse
from pathlib import Path

from config import load_config
from engine import SportsCompEngine
from nba.provider import NbaApiStatsProvider


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update an NBA stats workbook with combined regular season and playoff totals."
    )
    parser.add_argument("--input", required=True, help="Path to the source .xlsx workbook.")
    parser.add_argument("--output", default="Sports_Comp_Updated.xlsx", help="Path for the updated workbook.")
    parser.add_argument("--season", default="2025-26", help="NBA season, for example 2025-26.")
    parser.add_argument("--sheet", default=None, help="Optional worksheet name. Defaults to active sheet.")
    parser.add_argument("--config", default=None, help="Optional JSON config path.")
    parser.add_argument("--cache", default="cache/sports_comp.sqlite3", help="SQLite cache path.")
    parser.add_argument("--report-dir", default="reports", help="Directory for update reports.")
    parser.add_argument("--min-score", type=int, default=88, help="Minimum fuzzy match score from 0 to 100.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    provider = NbaApiStatsProvider(cache_path=Path(args.cache), min_match_score=args.min_score)
    engine = SportsCompEngine(config=config, provider=provider, report_dir=Path(args.report_dir))

    result = engine.update_workbook(
        input_path=Path(args.input),
        output_path=Path(args.output),
        season=args.season,
        sheet_name=args.sheet,
    )

    print(f"Updated workbook: {result.output_path}")
    print(f"Matched players: {result.matched_count}")
    print(f"Unmatched players: {len(result.unmatched_players)}")
    print(f"Report JSON: {result.report_json}")
    print(f"Report CSV: {result.report_csv}")
    return 0 if not result.unmatched_players else 2


if __name__ == "__main__":
    raise SystemExit(main())

