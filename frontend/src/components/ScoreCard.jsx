function ScoreCard({
  title,
  value,
  icon = "📊",
  gradient = "linear-gradient(180deg, #2563eb, #7c3aed)"
}) {

  const cardStyle = {
    background: gradient,
    color: "white",
    borderRadius: "16px",
    padding: "24px",
    minHeight: "120px",
    boxShadow: "0 12px 40px rgba(0,0,0,0.45)",
    border: "1px solid rgba(148, 163, 184, 0.2)",
    transition: "all 0.3s ease",
    position: "relative",
    overflow: "hidden"
  };

  const iconStyle = {
    fontSize: "32px",
    marginBottom: "12px",
    opacity: "0.9"
  };

  const titleStyle = {
    fontSize: "14px",
    fontWeight: "600",
    marginBottom: "8px",
    opacity: "0.9",
    letterSpacing: "0.5px"
  };

  const valueStyle = {
    fontSize: "36px",
    fontWeight: "800",
    letterSpacing: "0.5px"
  };

  return (
    <div
      style={cardStyle}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-8px)";
        e.currentTarget.style.boxShadow = "0 20px 60px rgba(0,0,0,0.55)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "0 12px 40px rgba(0,0,0,0.45)";
      }}
    >
      <div style={iconStyle}>{icon}</div>
      <h3 style={titleStyle}>{title}</h3>
      <h1 style={valueStyle}>{value}</h1>
    </div>
  );
}

export default ScoreCard;