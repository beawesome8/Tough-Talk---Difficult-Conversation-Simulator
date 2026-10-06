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
