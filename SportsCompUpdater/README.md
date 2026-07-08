# SportsCompUpdater

SportsCompUpdater fills an NBA fantasy/stat spreadsheet from a workbook of player names.

It reads player names from column A, combines regular season and playoff totals for the selected season, writes the stat columns E through P, preserves formatting, and saves a new workbook plus an update report.

## What It Updates

By default the app writes these columns:

| Column | Stat |
| --- | --- |
| E | Points |
| F | Rebounds |
| G | Assists |
| H | Blocks |
| I | Steals |
| J | FT% |
| K | FG% |
| L | 3PM |
| M | FGA |
| N | FGM |
| O | FTA |
| P | FTM |

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py --input Sports_Comp.xlsx --output Sports_Comp_Updated.xlsx --season 2025-26
```

The app writes:

- `Sports_Comp_Updated.xlsx`
- `reports/update_report.json`
- `reports/update_report.csv`

## Notes

The provider uses the public `nba_api` package because it gives season-level regular season and playoff totals in one reliable table. The original chat mentioned ESPN, but ESPN does not expose a single stable combined-stat download for this workflow. If you still need an ESPN-only provider, this codebase is structured so a second provider can be added behind the same interface.

## Test

```bash
pytest
```

