import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();

  const navStyle = {
    background: "linear-gradient(90deg, #0f172a, #1e293b)",
    padding: "16px 24px",
    boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
    borderBottom: "1px solid rgba(148, 163, 184, 0.15)",
    position: "sticky",
    top: 0,
    zIndex: 100
  };

  const containerStyle = {
    maxWidth: "1400px",
    margin: "0 auto",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between"
  };

  const logoStyle = {
    color: "#60a5fa",
    fontWeight: "800",
    fontSize: "24px",
    textDecoration: "none",
    letterSpacing: "0.5px"
  };

  const linkContainerStyle = {
    display: "flex",
    gap: "12px"
  };

  const getLinkStyle = (path) => {
    const isActive = location.pathname === path;
    
    return {
      color: isActive ? "white" : "#94a3b8",
      textDecoration: "none",
      padding: "10px 18px",
      borderRadius: "8px",
      fontWeight: "600",
      transition: "all 0.25s ease",
      background: isActive 
        ? "linear-gradient(90deg, #2563eb, #7c3aed)" 
        : "transparent",
      boxShadow: isActive 
        ? "0 6px 16px rgba(37, 99, 235, 0.35)" 
        : "none"
    };
  };

  return (
    <nav style={navStyle}>
      <div style={containerStyle}>
        <Link to="/" style={logoStyle}>
          🛡️ GRC Platform
        </Link>

        <div style={linkContainerStyle}>
          <Link
            to="/"
            style={getLinkStyle("/")}
            onMouseEnter={(e) => {
              if (location.pathname !== "/") {
                e.currentTarget.style.background = "linear-gradient(90deg, #2563eb, #7c3aed)";
                e.currentTarget.style.color = "white";
                e.currentTarget.style.boxShadow = "0 6px 16px rgba(37, 99, 235, 0.25)";
              }
            }}
            onMouseLeave={(e) => {
              if (location.pathname !== "/") {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "#94a3b8";
                e.currentTarget.style.boxShadow = "none";
              }
            }}
          >
            📊 Dashboard
          </Link>

          <Link
            to="/scan"
            style={getLinkStyle("/scan")}
            onMouseEnter={(e) => {
              if (location.pathname !== "/scan") {
                e.currentTarget.style.background = "linear-gradient(90deg, #1fe4f5, #2563eb)";
                e.currentTarget.style.color = "#0f172a";
                e.currentTarget.style.boxShadow = "0 6px 16px rgba(37, 99, 235, 0.25)";
              }
            }}
            onMouseLeave={(e) => {
              if (location.pathname !== "/scan") {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "#94a3b8";
                e.currentTarget.style.boxShadow = "none";
              }
            }}
          >
            🔍 Scan Center
          </Link>

          <Link
            to="/findings"
            style={getLinkStyle("/findings")}
            onMouseEnter={(e) => {
              if (location.pathname !== "/findings") {
                e.currentTarget.style.background = "linear-gradient(90deg, #ef4444, #dc2626)";
                e.currentTarget.style.color = "white";
                e.currentTarget.style.boxShadow = "0 6px 16px rgba(239, 68, 68, 0.35)";
              }
            }}
            onMouseLeave={(e) => {
              if (location.pathname !== "/findings") {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "#94a3b8";
                e.currentTarget.style.boxShadow = "none";
              }
            }}
          >
            🚨 Findings
          </Link>

          <Link
            to="/compliance"
            style={getLinkStyle("/compliance")}
            onMouseEnter={(e) => {
              if (location.pathname !== "/compliance") {
                e.currentTarget.style.background = "linear-gradient(90deg, #10b981, #059669)";
                e.currentTarget.style.color = "white";
                e.currentTarget.style.boxShadow = "0 6px 16px rgba(16, 185, 129, 0.35)";
              }
            }}
            onMouseLeave={(e) => {
              if (location.pathname !== "/compliance") {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "#94a3b8";
                e.currentTarget.style.boxShadow = "none";
              }
            }}
          >
            📋 Compliance
          </Link>

          <Link
            to="/scans"
            style={getLinkStyle("/scans")}
            onMouseEnter={(e) => {
              if (location.pathname !== "/scans") {
                e.currentTarget.style.background = "linear-gradient(90deg, #fbbf24, #f59e0b)";
                e.currentTarget.style.color = "#0f172a";
                e.currentTarget.style.boxShadow = "0 6px 16px rgba(251, 191, 36, 0.35)";
              }
            }}
            onMouseLeave={(e) => {
              if (location.pathname !== "/scans") {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "#94a3b8";
                e.currentTarget.style.boxShadow = "none";
              }
            }}
          >
            📈 Scan History
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;