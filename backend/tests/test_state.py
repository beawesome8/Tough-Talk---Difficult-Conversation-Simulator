# backend/tests/test_state.py
from app.state import (
    apply_tags,
    atmosphere,
    clamp,
    is_short_closed,
    should_reveal,
)


def test_clamp_bounds():
    assert clamp(-5) == 0
    assert clamp(150) == 100
    assert clamp(50) == 50


def test_apply_tags_single_positive():
    trust, stress = apply_tags(40, 60, ["acknowledges_feelings"])
    assert trust == 48
    assert stress == 54


def test_apply_tags_single_negative():
    trust, stress = apply_tags(40, 60, ["dismisses_or_interrupts"])
    assert trust == 28
    assert stress == 68


def test_apply_tags_multiple_tags_sum():
    trust, stress = apply_tags(40, 60, ["asks_open_question", "names_specific_contribution"])
    assert trust == 40 + 6 + 7
    assert stress == 60 - 3 - 4


def test_apply_tags_clamps_at_bounds():
    trust, stress = apply_tags(95, 5, ["offers_concrete_support"])
    assert trust == 100
    assert stress == 0


def test_apply_tags_unknown_tag_ignored():
    trust, stress = apply_tags(40, 60, ["not_a_real_tag"])
    assert (trust, stress) == (40, 60)


def test_apply_tags_empty_list_unchanged():
    assert apply_tags(40, 60, []) == (40, 60)


def test_atmosphere_thresholds():
    assert atmosphere(0) == "guarded"
    assert atmosphere(39) == "guarded"
    assert atmosphere(40) == "neutral"
    assert atmosphere(64) == "neutral"
    assert atmosphere(65) == "open"
    assert atmosphere(100) == "open"


def test_should_reveal_requires_trust_threshold():
    assert should_reveal(64, ["asks_open_question"], already_revealed=False) is False


def test_should_reveal_requires_qualifying_tag():
    assert should_reveal(70, ["blames_or_generalises"], already_revealed=False) is False


def test_should_reveal_fires_with_open_question():
    assert should_reveal(65, ["asks_open_question"], already_revealed=False) is True


def test_should_reveal_fires_with_acknowledges_feelings():
    assert should_reveal(80, ["acknowledges_feelings"], already_revealed=False) is True


def test_should_reveal_never_fires_twice():
    assert should_reveal(90, ["asks_open_question"], already_revealed=True) is False


def test_is_short_closed_threshold():
    assert is_short_closed(80) is False
    assert is_short_closed(81) is True
