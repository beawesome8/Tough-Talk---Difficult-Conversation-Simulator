const COPY = {
  guarded: { label: "Guarded", color: "var(--guarded)", tint: "var(--guarded-tint)" },
  neutral: { label: "Neutral", color: "var(--neutral)", tint: "var(--neutral-tint)" },
  open: { label: "Open", color: "var(--open)", tint: "var(--open-tint)" },
};

export default function AtmosphereIndicator({ level }) {
  const info = COPY[level] || COPY.neutral;
  return (
    <div
      className="atmosphere"
      style={{ background: info.tint, color: info.color }}
    >
      <span className="atmosphere-dot" style={{ background: info.color }} />
      {info.label}
    </div>
  );
}
