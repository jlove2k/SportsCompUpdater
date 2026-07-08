from openpyxl import Workbook

from excel.parser import read_player_rows
from excel.updater import write_player_stats
from nba.stats import PlayerStats


def test_reads_player_names_from_column_a():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "Player"
    sheet["A2"] = "Player One"
    sheet["A3"] = ""
    sheet["A4"] = "Player Two"

    rows = read_player_rows(sheet)

    assert [row.name for row in rows] == ["Player One", "Player Two"]
    assert [row.row_number for row in rows] == [2, 4]


def test_writes_stats_to_configured_columns_only():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A2"] = "Player One"
    sheet["D2"] = "keep"
    stats = PlayerStats(points=1, rebounds=2, assists=3, blocks=4, steals=5, ft_pct=0.8, fg_pct=0.5, three_pm=6, fga=7, fgm=8, fta=9, ftm=10)

    write_player_stats(
        sheet,
        2,
        stats,
        {
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
        },
    )

    assert sheet["D2"].value == "keep"
    assert sheet["E2"].value == 1
    assert sheet["P2"].value == 10

