import time

from app import session_store
from app.models import Turn


def test_create_session_has_default_state():
    session = session_store.create_session()
    assert session.trust == 40
    assert session.stress == 60
    assert session.concern_revealed is False
    assert session.turns == []
    assert session.ended is False


def test_save_and_get_round_trip():
    session = session_store.create_session()
    session.trust = 55
    session_store.save_session(session)

    fetched = session_store.get_session(session.session_id)
    assert fetched is not None
    assert fetched.trust == 55


def test_get_unknown_session_returns_none():
    assert session_store.get_session("does-not-exist") is None


def test_get_expired_session_returns_none(monkeypatch):
    session = session_store.create_session()
    session_store.save_session(session)

    future = time.time() + session_store.SESSION_TTL_SECONDS + 1
    monkeypatch.setattr(time, "time", lambda: future)

    assert session_store.get_session(session.session_id) is None


def test_turn_records_before_and_after_values():
    turn = Turn(
        leader_message="What's going on?",
        sam_reply="Honestly, it's been a lot.",
        tags=["asks_open_question"],
        trust_before=40,
        trust_after=46,
        stress_before=60,
        stress_after=57,
    )
    assert turn.trust_after - turn.trust_before == 6
