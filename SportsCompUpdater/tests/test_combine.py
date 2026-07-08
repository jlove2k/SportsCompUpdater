from nba.combine import combine_player_stats


def test_combine_regular_season_and_playoff_rows():
    rows = [
        {
            "PLAYER_NAME": "Test Player",
            "PTS": 100,
            "REB": 40,
            "AST": 30,
            "BLK": 5,
            "STL": 6,
            "FG3M": 10,
            "FGA": 80,
            "FGM": 40,
            "FTA": 20,
            "FTM": 15,
        },
        {
            "PLAYER_NAME": "Test Player",
            "PTS": 20,
            "REB": 8,
            "AST": 4,
            "BLK": 1,
            "STL": 2,
            "FG3M": 3,
            "FGA": 10,
            "FGM": 5,
            "FTA": 4,
            "FTM": 3,
        },
    ]

    stats = combine_player_stats(rows)["Test Player"]

    assert stats.points == 120
    assert stats.rebounds == 48
    assert stats.assists == 34
    assert stats.blocks == 6
    assert stats.steals == 8
    assert stats.three_pm == 13
    assert stats.fga == 90
    assert stats.fgm == 45
    assert stats.fta == 24
    assert stats.ftm == 18
    assert stats.fg_pct == 0.5
    assert stats.ft_pct == 0.75

