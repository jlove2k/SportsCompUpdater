from nba.normalize import normalize_name


def test_normalize_name_removes_accents_suffix_and_punctuation():
    assert normalize_name("Nikola Jovic Jr.") == "nikola jovic"
    assert normalize_name("D'Angelo Russell") == "dangelo russell"

