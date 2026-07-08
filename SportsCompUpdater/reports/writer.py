from __future__ import annotations

import csv
import json
from pathlib import Path


def write_reports(
    report_dir: Path,
    matched: list[dict[str, object]],
    unmatched: list[dict[str, object]],
) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "update_report.json"
    csv_path = report_dir / "update_report.csv"

    payload = {
        "matched_count": len(matched),
        "unmatched_count": len(unmatched),
        "matched": matched,
        "unmatched": unmatched,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["status", "row", "workbook_name", "matched_name", "score"])
        writer.writeheader()
        for item in matched:
            writer.writerow(
                {
                    "status": "matched",
                    "row": item["row"],
                    "workbook_name": item["workbook_name"],
                    "matched_name": item["matched_name"],
                    "score": item["score"],
                }
            )
        for item in unmatched:
            writer.writerow(
                {
                    "status": "unmatched",
                    "row": item["row"],
                    "workbook_name": item["name"],
                    "matched_name": "",
                    "score": "",
                }
            )

    return json_path, csv_path

