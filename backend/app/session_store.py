"""In-memory session storage. No persistence, no logging of message content
beyond what the Session object itself holds for the life of the process."""
import time
import uuid

from app.models import Session

SESSION_TTL_SECONDS = 1800
MAX_TURNS = 12

_sessions: dict[str, Session] = {}


def create_session() -> Session:
    now = time.time()
    session = Session(session_id=str(uuid.uuid4()), created_at=now, last_active=now)
    _sessions[session.session_id] = session
    return session


def get_session(session_id: str) -> Session | None:
    session = _sessions.get(session_id)
    if session is None:
        return None
    if time.time() - session.last_active > SESSION_TTL_SECONDS:
        del _sessions[session_id]
        return None
    return session


def save_session(session: Session) -> None:
    session.last_active = time.time()
    _sessions[session.session_id] = session
