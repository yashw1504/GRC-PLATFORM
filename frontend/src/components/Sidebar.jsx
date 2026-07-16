import { Link } from "react-router-dom";

function Sidebar() {
  const sidebarStyle = {
    width: "240px",
    background: "linear-gradient(180deg, #ffffff, #f8fafc)",
    padding: "20px",
    minHeight: "100vh",
    boxShadow: "0 8px 32px rgba(15, 23, 42, 0.08)",
    borderRight: "1px solid #e2e8f0",
  };

  const titleStyle = {
    color: "#1e3a8a",
    fontWeight: "800",
    fontSize: "22px",
    marginBottom: "24px",
    letterSpacing: "0.5px",
    textAlign: "center",
  };

  const linkStyle = {
    color: "#334155",
    textDecoration: "none",
    padding: "14px 16px",
    display: "block",
    borderRadius: "10px",
    marginBottom: "8px",
    fontWeight: "600",
    transition: "all 0.25s ease",
    border: "1px solid transparent",
    background: "transparent",
  };

  return (
    <div style={sidebarStyle}>
      <h2 style={titleStyle}>🛡️ GRC Platform</h2>

      <hr
        style={{
          border: "none",
          height: "1px",
          background: "linear-gradient(90deg, rgba(148, 163, 184, 0.25), rgba(148, 163, 184, 0.08))",
          marginBottom: "20px",
        }}
      />

      <Link
        to="/"
        style={{
          ...linkStyle,
          background: "linear-gradient(90deg, #2563eb, #7c3aed)",
          color: "white",
          boxShadow: "0 6px 16px rgba(37, 99, 235, 0.18)",
        }}
      >
        📊 Dashboard
      </Link>

      <Link
        to="/scan"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #dbeafe, #bfdbfe)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(37, 99, 235, 0.12)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#334155";
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.transform = "translateX(0)";
        }}
      >
        🔍 Scan Center
      </Link>

      <Link
        to="/assets"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #ede9fe, #ddd6fe)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(139, 92, 246, 0.12)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#334155";
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.transform = "translateX(0)";
        }}
      >
        🖥️ Assets
      </Link>

      <Link
        to="/credentials"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #cffafe, #dbeafe)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(6, 182, 212, 0.12)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#334155";
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.transform = "translateX(0)";
        }}
      >
        🔐 Credentials
      </Link>

      <Link
        to="/findings"
        style={linkStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "linear-gradient(90deg, #fee2e2, #fecaca)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(239, 68, 68, 0.12)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#334155";
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
          e.currentTarget.style.background = "linear-gradient(90deg, #dcfce7, #bbf7d0)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(16, 185, 129, 0.12)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#334155";
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
          e.currentTarget.style.background = "linear-gradient(90deg, #fef3c7, #fde68a)";
          e.currentTarget.style.color = "#0f172a";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(245, 158, 11, 0.12)";
          e.currentTarget.style.transform = "translateX(4px)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.color = "#334155";
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