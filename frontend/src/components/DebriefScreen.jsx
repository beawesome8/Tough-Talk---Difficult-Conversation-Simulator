function TrustTimeline({ timeline }) {
  if (timeline.length === 0) return <p>No turns recorded.</p>;
  const width = 600;
  const height = 120;
  const max = 100;
  const points = timeline
    .map((value, i) => {
      const x = (i / Math.max(timeline.length - 1, 1)) * width;
      const y = height - (value / max) * height;
      return `${x},${y}`;
    })
    .join(" ");
  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: "100%", maxWidth: 600 }}>
      <polyline points={points} fill="none" stroke="#2f6f4f" strokeWidth="3" />
    </svg>
  );
}

export default function DebriefScreen({ debrief, onRestart }) {
  const { timeline, top_turns, concern_revealed, concern_revealed_turn, suggestions } = debrief;
  return (
    <div className="screen">
      <h2>Debrief</h2>

      <h3>Trust over the conversation</h3>
      <TrustTimeline timeline={timeline} />

      <h3>Moments that moved trust the most</h3>
      {top_turns.map((turn, i) => (
        <div key={i} style={{ marginBottom: 12, padding: 12, background: "#eee", borderRadius: 8 }}>
          <p style={{ margin: 0 }}>
            <em>"{turn.quote}"</em>
          </p>
          <p style={{ margin: "4px 0 0", fontSize: "0.9rem" }}>
            Tags: {turn.tag_summary.join(", ") || "none"} — trust change:{" "}
            {turn.trust_change > 0 ? "+" : ""}
            {turn.trust_change}
          </p>
        </div>
      ))}

      <h3>Sam's hidden concern</h3>
      <p>
        {concern_revealed
          ? `Came out at turn ${concern_revealed_turn}, after trust was high enough and you asked an open question or acknowledged how Sam felt.`
          : "Did not come out this time — trust didn't reach the point where Sam felt safe sharing it."}
      </p>

      <h3>Two things to try next time</h3>
      <ul>
        {suggestions.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>

      <button onClick={onRestart}>Start a new conversation</button>
    </div>
  );
}
