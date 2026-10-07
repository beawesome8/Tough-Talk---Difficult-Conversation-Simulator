# backend/app/scenario.py
"""Fixed scenario content for v0.1. Sam is fictional; see README."""

SAM_PERSONA = (
    "You are Sam, a strong engineer on the leader's team. Sam has missed two "
    "deadlines recently. After a colleague left the team, Sam quietly absorbed "
    "that colleague's workload without telling anyone. Sam is proud, "
    "hard-working, and not naturally someone who volunteers how they feel."
)

HIDDEN_CONCERN = (
    "Sam feels the extra workload has gone completely unnoticed, and has "
    "started seriously thinking about leaving the team."
)

TAG_DEFINITIONS = {
    "acknowledges_feelings": "Explicitly names or validates an emotion or state Sam might be in (e.g. stressed, overwhelmed, stretched thin), without judging it. Requires the feeling/state to be named outright in words, not merely implied by an offer of help alone.",
    "asks_open_question": "Asks a genuine question inviting Sam to explain, that isn't answerable yes/no.",
    "names_specific_contribution": "Names a specific, concrete action or thing Sam did or took on (e.g. 'picked up a whole second role', 'the script you wrote'). Does not apply to a vague reference to being busy/overloaded ('covering a lot') or to a negative fact like a missed deadline — the thing named must be a distinct, nameable action, not a mood or a failure.",
    "offers_concrete_support": "Offers a specific, actionable form of help (not a vague 'let me know').",
    "blames_or_generalises": "Blames Sam personally for a failure or shortcoming, or generalises negatively about Sam's behaviour ('you always', 'you never'), in an accusatory tone. Does NOT apply to a sympathetic description of an unfair burden or circumstance Sam is in, even one phrased starkly (e.g. noting Sam took on work 'without anyone asking' is describing an unrecognised burden, not blaming Sam).",
    "dismisses_or_interrupts": "Dismisses, minimises, cuts Sam off, or refuses to engage with what Sam might say. If this applies, do NOT also apply adds_pressure_without_support, even if the message also mentions a deadline or urgency — the two tags are mutually exclusive.",
    "adds_pressure_without_support": "Adds urgency or a demand without offering any help or resource. Mutually exclusive with dismisses_or_interrupts: if the message cuts Sam off, refuses to engage, or is otherwise dismissive, tag only dismisses_or_interrupts, never both.",
}

OPENING_LINE = "Hey — thanks for making time. What did you want to talk about?"
