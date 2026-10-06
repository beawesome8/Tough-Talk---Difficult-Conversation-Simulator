const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function postJSON(path, body) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || `Request to ${path} failed`);
  }
  return response.json();
}

export function startSession() {
  return postJSON("/session");
}

export function sendTurn(sessionId, message) {
  return postJSON("/turn", { session_id: sessionId, message });
}

export function endSession(sessionId) {
  return postJSON("/end", { session_id: sessionId });
}
