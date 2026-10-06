# backend/tests/test_tagging.py
import os

import pytest

from app.anthropic_client import tag_message
from tests.golden_set import GOLDEN_SET

requires_api_key = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; skipping live model test",
)


@requires_api_key
def test_tagging_accuracy_at_least_10_of_12():
    correct = 0
    for case in GOLDEN_SET:
        actual_tags = set(tag_message(case["message"]))
        if actual_tags == case["expected_tags"]:
            correct += 1
    assert correct >= 10, f"only {correct}/12 messages tagged exactly as expected"
