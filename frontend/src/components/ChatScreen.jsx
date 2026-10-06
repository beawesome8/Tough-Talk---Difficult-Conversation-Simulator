import { useRef, useState } from "react";
import { endSession, sendTurn } from "../api.js";
import AtmosphereIndicator from "./AtmosphereIndicator.jsx";

export default function ChatScreen({ sessionId, openingLine, onEnded }) {
  const [messages, setMessages] = useState([{ from: "sam", text: openingLine }]);
  const [atmosphere, setAtmosphere] = useState("neutral");
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(false);
  const [ended, setEnded] = useState(false);
  const endingRef = useRef(false);

  async function finishConversation() {
    if (endingRef.current) return;
    endingRef.current = true;
    const debrief = await endSession(sessionId);
    onEnded(debrief);
  }

  async function handleSend() {
    const text = draft.trim();
    if (!text || loading || ended) return;
    setMessages((prev) => [...prev, { from: "leader", text }]);
    setDraft("");
    setLoading(true);
    try {
      const result = await sendTurn(sessionId, text);
      setMessages((prev) => [...prev, { from: "sam", text: result.reply }]);
      setAtmosphere(result.atmosphere);
      if (result.ended) {
        setEnded(true);
        await finishConversation();
      }
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") handleSend();
  }

  return (
    <div className="screen">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Conversation with Sam</h2>
        <AtmosphereIndicator level={atmosphere} />
      </div>
      <div style={{ minHeight: 280, marginBottom: 12 }}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              textAlign: m.from === "leader" ? "right" : "left",
              margin: "8px 0",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 12,
                background: m.from === "leader" ? "#2f6f4f" : "#eee",
                color: m.from === "leader" ? "white" : "#222",
                maxWidth: "80%",
              }}
            >
              {m.text}
            </span>
          </div>
        ))}
        {loading && <p>Sam is thinking…</p>}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          type="text"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message…"
          disabled={loading || ended}
        />
        <button onClick={handleSend} disabled={loading || ended}>
          Send
        </button>
      </div>
      <p style={{ marginTop: 16 }}>
        <button onClick={finishConversation} disabled={loading || ended}>
          End conversation
        </button>
      </p>
    </div>
  );
}
