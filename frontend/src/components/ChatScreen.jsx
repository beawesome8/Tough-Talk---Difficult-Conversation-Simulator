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
      <div className="card">
        <div className="chat-header">
          <h2>Conversation with Sam</h2>
          <AtmosphereIndicator level={atmosphere} />
        </div>
        <div className="chat-log">
          {messages.map((m, i) => (
            <div key={i} className={`message-row ${m.from}`}>
              <div className={`avatar ${m.from}`}>{m.from === "leader" ? "Y" : "S"}</div>
              <div className={`bubble ${m.from}`}>{m.text}</div>
            </div>
          ))}
          {loading && (
            <div className="message-row sam">
              <div className="avatar sam">S</div>
              <div className="bubble sam typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>
        <div className="composer">
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
        <div className="actions-row">
          <button className="secondary" onClick={finishConversation} disabled={loading || ended}>
            End conversation
          </button>
        </div>
      </div>
    </div>
  );
}
