# backend/tests/test_dialogue_prompt.py
from app.anthropic_client import build_system_prompt
from app.scenario import HIDDEN_CONCERN


def test_prompt_never_contains_hidden_concern_when_not_revealing():
    prompt = build_system_prompt("neutral", reveal_now=False, closed_answers=False)
    assert HIDDEN_CONCERN not in prompt


def test_prompt_contains_hidden_concern_only_when_revealing():
    prompt = build_system_prompt("open", reveal_now=True, closed_answers=False)
    assert HIDDEN_CONCERN in prompt


def test_prompt_never_contains_raw_numbers_section():
    prompt = build_system_prompt("guarded", reveal_now=False, closed_answers=True)
    assert "trust" not in prompt.lower()
    assert "stress" not in prompt.lower() or "short" in prompt.lower()


def test_prompt_instructs_short_closed_answers_when_flagged():
    prompt = build_system_prompt("neutral", reveal_now=False, closed_answers=True)
    assert "short" in prompt.lower()


def test_prompt_includes_atmosphere_label():
    prompt = build_system_prompt("open", reveal_now=False, closed_answers=False)
    assert "open" in prompt.lower()
