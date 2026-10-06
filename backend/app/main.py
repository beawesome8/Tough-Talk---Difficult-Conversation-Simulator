# backend/app/main.py
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import anthropic_client, rate_limit, session_store
from app.models import Turn
from app.scenario import OPENING_LINE
from app.state import apply_tags, atmosphere, is_short_closed, should_reveal

app = FastAPI(title="Tough Talk")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class StartResponse(BaseModel):
    session_id: str
    atmosphere: str
    opening_line: str


class TurnRequest(BaseModel):
    session_id: str
    message: str


class TurnResponse(BaseModel):
    reply: str
    atmosphere: str
    ended: bool


class EndRequest(BaseModel):
    session_id: str


class TopTurn(BaseModel):
    quote: str
    tag_summary: list[str]
    trust_change: int


class EndResponse(BaseModel):
    timeline: list[int]
    top_turns: list[TopTurn]
    concern_revealed: bool
    concern_revealed_turn: int | None
    suggestions: list[str]


def _enforce_limits(request: Request):
    ip = request.client.host if request.client else "unknown"
    if not rate_limit.check_daily_budget():
        raise HTTPException(status_code=503, detail="demo is resting for today, please try again tomorrow")
    if not rate_limit.check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="too many requests, please slow down")
    rate_limit.record_call()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/session", response_model=StartResponse)
def start_session(request: Request):
    _enforce_limits(request)
    session = session_store.create_session()
    return StartResponse(
        session_id=session.session_id,
        atmosphere=atmosphere(session.trust),
        opening_line=OPENING_LINE,
    )


@app.post("/turn", response_model=TurnResponse)
def take_turn(body: TurnRequest, request: Request):
    _enforce_limits(request)
    session = session_store.get_session(body.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found or expired")
    if session.ended or len(session.turns) >= session_store.MAX_TURNS:
        raise HTTPException(status_code=409, detail="conversation already ended")

    trust_before, stress_before = session.trust, session.stress
    tags = anthropic_client.tag_message(body.message)
    trust_after, stress_after = apply_tags(trust_before, stress_before, tags)
    reveal_now = should_reveal(trust_after, tags, session.concern_revealed)
    closed_answers = is_short_closed(stress_after)

    history = []
    for turn in session.turns[-3:]:
        history.append({"role": "user", "content": turn.leader_message})
        history.append({"role": "assistant", "content": turn.sam_reply})
    history.append({"role": "user", "content": body.message})

    reply = anthropic_client.get_sam_reply(
        atmosphere(trust_after), reveal_now, closed_answers, history
    )

    session.trust, session.stress = trust_after, stress_after
    if reveal_now:
        session.concern_revealed = True
        session.concern_revealed_turn = len(session.turns) + 1

    session.turns.append(
        Turn(
            leader_message=body.message,
            sam_reply=reply,
            tags=tags,
            trust_before=trust_before,
            trust_after=trust_after,
            stress_before=stress_before,
            stress_after=stress_after,
        )
    )
    ended = len(session.turns) >= session_store.MAX_TURNS
    session.ended = ended
    session_store.save_session(session)

    return TurnResponse(reply=reply, atmosphere=atmosphere(trust_after), ended=ended)


@app.post("/end", response_model=EndResponse)
def end_session(body: EndRequest):
    session = session_store.get_session(body.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found or expired")

    session.ended = True
    timeline = [turn.trust_after for turn in session.turns]

    ranked = sorted(session.turns, key=lambda t: abs(t.trust_after - t.trust_before), reverse=True)
    top_turns = [
        TopTurn(
            quote=turn.leader_message,
            tag_summary=turn.tags,
            trust_change=turn.trust_after - turn.trust_before,
        )
        for turn in ranked[:3]
    ]

    behaviour_counts: dict[str, int] = {}
    for turn in session.turns:
        for tag in turn.tags:
            behaviour_counts[tag] = behaviour_counts.get(tag, 0) + 1

    suggestions = anthropic_client.get_debrief_suggestions(behaviour_counts, session.concern_revealed)
    session_store.save_session(session)

    return EndResponse(
        timeline=timeline,
        top_turns=top_turns,
        concern_revealed=session.concern_revealed,
        concern_revealed_turn=session.concern_revealed_turn,
        suggestions=suggestions,
    )
