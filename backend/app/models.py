from dataclasses import dataclass, field


@dataclass
class Turn:
    leader_message: str
    sam_reply: str
    tags: list[str]
    trust_before: int
    trust_after: int
    stress_before: int
    stress_after: int


@dataclass
class Session:
    session_id: str
    trust: int = 40
    stress: int = 60
    concern_revealed: bool = False
    concern_revealed_turn: int | None = None
    turns: list[Turn] = field(default_factory=list)
    created_at: float = 0.0
    last_active: float = 0.0
    ended: bool = False
