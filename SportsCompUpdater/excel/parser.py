from __future__ import annotations

from dataclasses import dataclass

from openpyxl.worksheet.worksheet import Worksheet


@dataclass(frozen=True)
class PlayerRow:
    row_number: int
    name: str


def read_player_rows(sheet: Worksheet, player_column: str = "A", first_data_row: int = 2) -> list[PlayerRow]:
    rows: list[PlayerRow] = []
    for row_number in range(first_data_row, sheet.max_row + 1):
        raw_value = sheet[f"{player_column}{row_number}"].value
        if raw_value is None:
            continue

        name = str(raw_value).strip()
        if not name:
            continue

        rows.append(PlayerRow(row_number=row_number, name=name))
    return rows

