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
    "acknowledges_feelings": "Names or validates how the other person might feel, without judging it.",
    "asks_open_question": "Asks a genuine question inviting Sam to explain, that isn't answerable yes/no.",
    "names_specific_contribution": "Refers to a concrete, specific thing Sam did or is working on.",
    "offers_concrete_support": "Offers a specific, actionable form of help (not a vague 'let me know').",
    "blames_or_generalises": "Blames Sam personally or generalises ('you always', 'you never').",
    "dismisses_or_interrupts": "Dismisses, minimises, or talks over what Sam might say.",
    "adds_pressure_without_support": "Adds urgency or a demand without offering any help or resource.",
}

OPENING_LINE = "Hey — thanks for making time. What did you want to talk about?"
