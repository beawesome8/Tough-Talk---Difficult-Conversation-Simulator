# backend/app/anthropic_client.py
"""All Anthropic API calls live here. Tagging uses a small model with forced
tool-use so the output is structured JSON, never free text."""
import anthropic

from app.scenario import TAG_DEFINITIONS
from app.state import BEHAVIOUR_TAGS

TAGGING_MODEL = "claude-haiku-4-5-20251001"
DIALOGUE_MODEL = "claude-sonnet-5"

_client = anthropic.Anthropic()

_TAG_LINES = "\n".join(f"- {tag}: {desc}" for tag, desc in TAG_DEFINITIONS.items())

_TAGGING_TOOL = {
    "name": "tag_behaviours",
    "description": "Tag which behaviours a manager's message to a direct report shows.",
    "input_schema": {
        "type": "object",
        "properties": {
            "tags": {
                "type": "array",
                "items": {"type": "string", "enum": BEHAVIOUR_TAGS},
            }
        },
        "required": ["tags"],
    },
}


def tag_message(leader_message: str) -> list[str]:
    prompt = (
        "A manager just said this to a direct report during a difficult "
        "feedback conversation. Tag which of these behaviours it shows "
        f"(zero or more apply):\n{_TAG_LINES}\n\n"
        f'Message: "{leader_message}"'
    )
    response = _client.messages.create(
        model=TAGGING_MODEL,
        max_tokens=200,
        tools=[_TAGGING_TOOL],
        tool_choice={"type": "tool", "name": "tag_behaviours"},
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "tool_use":
            raw_tags = block.input.get("tags", [])
            valid = {t for t in BEHAVIOUR_TAGS}
            return list(dict.fromkeys(t for t in raw_tags if t in valid))
    return []
