"""Output-side check: Sam's reply must never leak the state model."""
import re

_LEAK_KEYWORDS = (
    "trust score",
    "system prompt",
    "my instructions",
    "stress level",
    "language model",
    "i'm an ai",
    "i am an ai",
    "\bsystem\b",
    "\bprompt\b",
)

_SCORE_NUMBER_RE = re.compile(r"\b\d{1,3}\s*(%|percent|points?|/\s*100)", re.IGNORECASE)

FALLBACK_LINE = "Let's stick to what's actually going on — what did you want to talk about?"


def contains_leak(text: str) -> bool:
    lowered = text.lower()
    for keyword in _LEAK_KEYWORDS:
        if re.search(keyword, lowered):
            return True
    return bool(_SCORE_NUMBER_RE.search(lowered))
