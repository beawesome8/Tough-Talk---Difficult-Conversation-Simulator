function TrustTimeline({ timeline }) {
  if (timeline.length === 0) return <p>No turns recorded.</p>;
  const width = 600;
  const height = 140;
  const max = 100;
  const yFor = (value) => height - (value / max) * height;
  const points = timeline
    .map((value, i) => {
      const x = (i / Math.max(timeline.length - 1, 1)) * width;
      return `${x},${yFor(value)}`;
    })
    .join(" ");
  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: "100%", maxWidth: 600, display: "block" }}>
      <rect x="0" y={yFor(100)} width={width} height={yFor(65) - yFor(100)} fill="#eaf3ee" />
      <rect x="0" y={yFor(64)} width={width} height={yFor(40) - yFor(64)} fill="#fbf3e1" />
      <rect x="0" y={yFor(39)} width={width} height={height - yFor(39)} fill="#fbece7" />
      <polyline points={points} fill="none" stroke="#2f6f4f" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
      {timeline.map((value, i) => {
        const x = (i / Math.max(timeline.length - 1, 1)) * width;
        return <circle key={i} cx={x} cy={yFor(value)} r="3.5" fill="#2f6f4f" />;
      })}
    </svg>
  );
}

export default function DebriefScreen({ debrief, onRestart }) {
  const { timeline, top_turns, concern_revealed, concern_revealed_turn, suggestions } = debrief;
  return (
    <div className="screen">
      <div className="card">
        <span className="eyebrow">Debrief</span>
        <h2>How it went</h2>

        <h3>Trust over the conversation</h3>
        <div className="timeline-card">
          <TrustTimeline timeline={timeline} />
        </div>

        <h3>Moments that moved trust the most</h3>
        {top_turns.map((turn, i) => {
          const direction = turn.trust_change >= 0 ? "up" : "down";
          return (
            <div key={i} className={`turn-card ${direction}`}>
              <p className="turn-quote">"{turn.quote}"</p>
              <p className="turn-meta">
                {turn.tag_summary.join(", ") || "no tags"} ·{" "}
                <span className={`trust-delta ${direction}`}>
                  {turn.trust_change > 0 ? "+" : ""}
                  {turn.trust_change}
                </span>
              </p>
            </div>
          );
        })}

        <h3>Sam's hidden concern</h3>
        <p>
          {concern_revealed
            ? `Came out at turn ${concern_revealed_turn}, after trust was high enough and you asked an open question or acknowledged how Sam felt.`
            : "Did not come out this time — trust didn't reach the point where Sam felt safe sharing it."}
        </p>

        <h3>Two things to try next time</h3>
        <ul className="suggestion-list">
          {suggestions.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>

        <div className="actions-row">
          <button onClick={onRestart}>Start a new conversation</button>
        </div>
      </div>
    </div>
  );
}
