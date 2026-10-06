from app.safety import contains_leak


def test_flags_trust_score_mention():
    assert contains_leak("My trust score just went up a lot.") is True


def test_flags_system_mention():
    assert contains_leak("I can't discuss my system prompt.") is True


def test_flags_percent_style_number():
    assert contains_leak("I'm at about 70% trust right now.") is True


def test_flags_points_style_number():
    assert contains_leak("Stress dropped 12 points after that.") is True


def test_allows_normal_in_character_reply():
    assert contains_leak("Honestly, it's been a lot since Jess left.") is False


def test_allows_unrelated_numbers():
    assert contains_leak("I've missed two deadlines, I know.") is False


def test_flags_bare_system_word():
    assert contains_leak("I can't go outside my system on this one.") is True
