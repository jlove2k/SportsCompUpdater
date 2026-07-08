from nba.matcher import match_player_name
from nba.stats import PlayerStats


def test_exact_normalized_match():
    stats = {"LeBron James": PlayerStats(points=10)}
    match = match_player_name("Lebron James", stats)

    assert match is not None
    assert match.player_name == "LeBron James"
    assert match.score == 100


def test_rejects_low_score_match():
    stats = {"LeBron James": PlayerStats(points=10)}
    match = match_player_name("Stephen Curry", stats, min_score=95)

    assert match is None

