# backend/tests/test_endpoints.py
from fastapi.testclient import TestClient

from app import anthropic_client, session_store
from app.main import app

client = TestClient(app)


def test_full_conversation_flow(monkeypatch):
    monkeypatch.setattr(anthropic_client, "tag_message", lambda msg: ["asks_open_question"])
    monkeypatch.setattr(
        anthropic_client, "get_sam_reply", lambda *a, **k: "It's been a lot lately, honestly."
    )
    monkeypatch.setattr(
        anthropic_client, "get_debrief_suggestions", lambda *a, **k: ["Ask more often.", "Offer help sooner."]
    )

    start = client.post("/session")
    assert start.status_code == 200
    session_id = start.json()["session_id"]
    assert start.json()["atmosphere"] == "neutral"

    turn = client.post("/turn", json={"session_id": session_id, "message": "What's going on?"})
    assert turn.status_code == 200
    body = turn.json()
    assert body["reply"] == "It's been a lot lately, honestly."
    assert body["ended"] is False

    end = client.post("/end", json={"session_id": session_id})
    assert end.status_code == 200
    end_body = end.json()
    assert end_body["timeline"] == [46]
    assert len(end_body["suggestions"]) == 2
    assert end_body["top_turns"][0]["quote"] == "What's going on?"


def test_turn_on_unknown_session_returns_404(monkeypatch):
    response = client.post("/turn", json={"session_id": "nope", "message": "hi"})
    assert response.status_code == 404


def test_twelfth_turn_sets_ended_true(monkeypatch):
    monkeypatch.setattr(anthropic_client, "tag_message", lambda msg: [])
    monkeypatch.setattr(anthropic_client, "get_sam_reply", lambda *a, **k: "Okay.")

    start = client.post("/session")
    session_id = start.json()["session_id"]

    for _ in range(11):
        response = client.post("/turn", json={"session_id": session_id, "message": "go on"})
        assert response.json()["ended"] is False

    last = client.post("/turn", json={"session_id": session_id, "message": "last one"})
    assert last.json()["ended"] is True

    blocked = client.post("/turn", json={"session_id": session_id, "message": "one more"})
    assert blocked.status_code == 409


def test_reveal_fires_and_is_recorded_through_turn_endpoint(monkeypatch):
    monkeypatch.setattr(
        anthropic_client, "tag_message", lambda msg: ["acknowledges_feelings", "asks_open_question"]
    )
    monkeypatch.setattr(anthropic_client, "get_sam_reply", lambda *a, **k: "I hear you.")
    monkeypatch.setattr(
        anthropic_client, "get_debrief_suggestions", lambda *a, **k: ["Listen more."]
    )

    start = client.post("/session")
    assert start.status_code == 200
    session_id = start.json()["session_id"]

    # Turn 1: trust 40 + 8 + 6 = 54 (< 65, no reveal)
    turn1 = client.post("/turn", json={"session_id": session_id, "message": "I'm struggling"})
    assert turn1.status_code == 200
    assert turn1.json()["atmosphere"] == "neutral"

    # Turn 2: trust 54 + 8 + 6 = 68 (>= 65, both tags in REVEAL_TAGS, reveal fires)
    turn2 = client.post("/turn", json={"session_id": session_id, "message": "Really tough"})
    assert turn2.status_code == 200
    assert turn2.json()["atmosphere"] == "open"

    # Verify concern_revealed is recorded at /end
    end = client.post("/end", json={"session_id": session_id})
    assert end.status_code == 200
    end_body = end.json()
    assert end_body["concern_revealed"] is True
    assert end_body["concern_revealed_turn"] == 2
    assert end_body["timeline"] == [54, 68]
