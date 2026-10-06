"""Pure state-engine functions. No model calls, no I/O — see spec section 5."""

BEHAVIOUR_EFFECTS: dict[str, tuple[int, int]] = {
    "acknowledges_feelings": (8, -6),
    "asks_open_question": (6, -3),
    "names_specific_contribution": (7, -4),
    "offers_concrete_support": (8, -8),
    "blames_or_generalises": (-10, 10),
    "dismisses_or_interrupts": (-12, 8),
    "adds_pressure_without_support": (-6, 12),
}

BEHAVIOUR_TAGS: list[str] = list(BEHAVIOUR_EFFECTS.keys())

REVEAL_TAGS = {"asks_open_question", "acknowledges_feelings"}


def clamp(value: int) -> int:
    return max(0, min(100, value))


def apply_tags(trust: int, stress: int, tags: list[str]) -> tuple[int, int]:
    for tag in tags:
        d_trust, d_stress = BEHAVIOUR_EFFECTS.get(tag, (0, 0))
        trust += d_trust
        stress += d_stress
    return clamp(trust), clamp(stress)


def atmosphere(trust: int) -> str:
    if trust < 40:
        return "guarded"
    if trust < 65:
        return "neutral"
    return "open"


def should_reveal(trust: int, tags: list[str], already_revealed: bool) -> bool:
    if already_revealed or trust < 65:
        return False
    return any(tag in REVEAL_TAGS for tag in tags)


def is_short_closed(stress: int) -> bool:
    return stress > 80
