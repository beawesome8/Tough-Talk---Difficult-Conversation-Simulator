const COPY = {
  guarded: { label: "Guarded", color: "#b5533c" },
  neutral: { label: "Neutral", color: "#b08a2e" },
  open: { label: "Open", color: "#2f6f4f" },
};

export default function AtmosphereIndicator({ level }) {
  const info = COPY[level] || COPY.neutral;
  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        padding: "6px 12px",
        borderRadius: 20,
        border: `1px solid ${info.color}`,
        color: info.color,
        fontSize: "0.9rem",
      }}
    >
      <span style={{ width: 10, height: 10, borderRadius: "50%", background: info.color }} />
      Atmosphere: {info.label}
    </div>
  );
}
