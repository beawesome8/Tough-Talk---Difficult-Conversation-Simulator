# backend/tests/test_state_direction.py
import os

import pytest

from app.anthropic_client import get_sam_reply, tag_message
from app.state import apply_tags, atmosphere, should_reveal
from tests.golden_set import GOLDEN_SET

requires_api_key = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; skipping live model test",
)

GOOD_CONVERSATION = [m["message"] for m in GOLDEN_SET if m["trust_direction"] == "up"]
BAD_CONVERSATION = [m["message"] for m in GOLDEN_SET if m["trust_direction"] == "down"]


def _run_conversation(messages: list[str]) -> tuple[int, bool]:
    trust, stress, revealed = 40, 60, False
    history: list[dict] = []
    for message in messages:
        tags = tag_message(message)
        trust, stress = apply_tags(trust, stress, tags)
        reveal_now = should_reveal(trust, tags, revealed)
        if reveal_now:
            revealed = True
        history.append({"role": "user", "content": message})
        reply = get_sam_reply(atmosphere(trust), reveal_now, stress > 80, history)
        history.append({"role": "assistant", "content": reply})
    return trust, revealed


@requires_api_key
def test_good_conversation_ends_with_high_trust_and_reveal():
    trust, revealed = _run_conversation(GOOD_CONVERSATION)
    assert trust > 65
    assert revealed is True


@requires_api_key
def test_bad_conversation_ends_with_low_trust_and_no_reveal():
    trust, revealed = _run_conversation(BAD_CONVERSATION)
    assert trust < 30
    assert revealed is False
