import { Link } from "react-router-dom";

function Sidebar() {
  const sidebarStyle = {
    width: "240px",
    background: "linear-gradient(180deg, #0f172a, #1e293b)",
    padding: "20px",
    minHeight: "100vh",
    boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
    borderRight: "1px solid rgba(148, 163, 184, 0.15)"
  };

  const titleStyle = {
    color: "#60a5fa",
    fontWeight: "800",
    fontSize: "22px",
    marginBottom: "24px",
    letterSpacing: "0.5px",
    textAlign: "center"
  };

  const linkStyle = {
    color: "#e2e8f0",
    textDecoration: "none",
    padding: "14px 16px",
    display: "block",
    borderRadius: "10px",
    marginBottom: "8px",
    fontWeight: "600",
    transition: "all 0.25s ease",
    border: "1px solid transparent"
  };

  const getHoverStyle = (gradient) => ({
    ...linkStyle,
    "&:hover": {
      background: gradient,
      color: "white",
      boxShadow: "0 6px 20px rgba(37, 99, 235, 0.35)",
      transform: "translateX(4px)",
      border: "1px solid rgba(148, 163, 184, 0.2)"
    }
  });

  return (
    <div style={sidebarStyle}>
      <h2 style={titleStyle}>
        🛡️ GRC Platform
      </h2>

      <hr
        style={{
          border: "none",
          height: "1px",
          background: "linear-gradient(90deg, rgba(148, 163, 184, 0.3), rgba(148, 163, 184, 0.1))",
          marginBottom: "20px"
        }}
      />

      <Link
        to="/"
        style={{
          ...linkStyle,
          background: "linear-gradient(90deg, #2563eb, #7c3aed)",
          color: "white",
          boxShadow: "0 6px 16px rgba(37, 99, 235, 0.35)"
        }}
      >
        📊 Dashboard
      </Link>

      <Link
        to="/scan"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #1fe4f5, #2563eb)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(37, 99, 235, 0.25)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#e2e8f0";
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.transform = "translateX(0)";
        }}
      >
        🔍 Scan Center
      </Link>

      <Link
        to="/findings"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #ef4444, #dc2626)";
          e.currentTarget.style.color = "white";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(239, 68, 68, 0.35)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#e2e8f0";
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.transform = "translateX(0)";
        }}
      >
        🚨 Findings
      </Link>

      <Link
        to="/compliance"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #10b981, #059669)";
          e.currentTarget.style.color = "white";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(16, 185, 129, 0.35)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#e2e8f0";
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.transform = "translateX(0)";
        }}
      >
        📋 Compliance
      </Link>

      <Link
        to="/scans"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #fbbf24, #f59e0b)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(251, 191, 36, 0.35)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#e2e8f0";
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.transform = "translateX(0)";
        }}
      >
        📈 Scan History
      </Link>
    </div>
  );
}

export default Sidebar;