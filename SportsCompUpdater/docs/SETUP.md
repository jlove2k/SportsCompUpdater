# Setup Guide

## Create a GitHub Repository

1. Create a repository named `SportsCompUpdater`.
2. Keep it private if the workbook contains personal or league information.
3. Add these source files to the repository.
4. Commit the first version.

## First Local Run

Place your workbook beside `app.py`, then run:

```bash
python app.py --input Sports_Comp.xlsx --output Sports_Comp_Updated.xlsx --season 2025-26
```

If some names are unmatched, open `reports/update_report.csv`, fix the spelling in the workbook or lower `--min-score`, then run again.

