# backend/tests/golden_set.py
"""12 scripted leader messages with expected tags and expected trust direction.
Used by Test 1 (tagging accuracy) and Test 2 (state direction, Phase 3)."""

GOLDEN_SET = [
    {
        "message": "I noticed you've been covering a lot since the team shrank — how are you holding up with that?",
        "expected_tags": {"acknowledges_feelings", "asks_open_question"},
        "trust_direction": "up",
    },
    {
        "message": "You missed the last two deadlines, what's going on?",
        "expected_tags": {"asks_open_question"},
        "trust_direction": "up",
    },
    {
        "message": "The migration script you wrote last week fixed a real problem, that was good work.",
        "expected_tags": {"names_specific_contribution"},
        "trust_direction": "up",
    },
    {
        "message": "I can take two of your tickets off your plate this week so you have room to breathe.",
        "expected_tags": {"offers_concrete_support"},
        "trust_direction": "up",
    },
    {
        "message": "You always miss deadlines, this is a pattern with you.",
        "expected_tags": {"blames_or_generalises"},
        "trust_direction": "down",
    },
    {
        "message": "I don't have time for excuses right now, just get it done.",
        "expected_tags": {"dismisses_or_interrupts"},
        "trust_direction": "down",
    },
    {
        "message": "This needs to be done by Friday no matter what else is going on.",
        "expected_tags": {"adds_pressure_without_support"},
        "trust_direction": "down",
    },
    {
        "message": "Stop, I don't want to hear the backstory, just tell me when it'll be done.",
        "expected_tags": {"dismisses_or_interrupts"},
        "trust_direction": "down",
    },
    {
        "message": "What's actually been making this hard for you lately?",
        "expected_tags": {"asks_open_question"},
        "trust_direction": "up",
    },
    {
        "message": "It makes sense you're stretched thin, you picked up a whole second role without anyone asking.",
        "expected_tags": {"acknowledges_feelings", "names_specific_contribution"},
        "trust_direction": "up",
    },
    {
        "message": "Everyone else manages their workload fine, I don't see why you can't.",
        "expected_tags": {"blames_or_generalises"},
        "trust_direction": "down",
    },
    {
        "message": "Let's figure out together what support would actually help here — what would make the biggest difference?",
        "expected_tags": {"asks_open_question", "offers_concrete_support"},
        "trust_direction": "up",
    },
]
