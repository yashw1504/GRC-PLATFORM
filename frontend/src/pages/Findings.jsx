import { useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";

function Findings() {
  const [findings, setFindings] = useState([]);
  const [severityFilter, setSeverityFilter] = useState("All");
  const [scanFilter, setScanFilter] = useState("");
  const [urlFilter, setUrlFilter] = useState("");
  const [searchText, setSearchText] = useState("");
  const [debugData, setDebugData] = useState(null);

  useEffect(() => {
    API.get("/findings")
      .then((response) => {
        console.log("=== API RESPONSE ===", response);
        console.log("=== API DATA ===", response.data);
        
        // Check if data is nested (e.g., response.data.findings)
        const actualData = response.data.findings || response.data.findings_set || response.data;
        
        console.log("=== ACTUAL FINDINGS DATA ===", actualData);
        console.log("=== FIRST FINDING ===", actualData[0]);
        
        // Log all keys of first finding
        if (actualData[0]) {
          console.log("=== FIRST FINDING KEYS ===", Object.keys(actualData[0]));
        }
        
        setFindings(actualData);
        setDebugData(actualData[0]);
      })
      .catch(console.error);
  }, []);

  console.log("=== CURRENT FINDINGS STATE ===", findings);

  // Extract unique scans - trying ALL possible field names
  const uniqueScans = findings
    .map(f => f.scan_id || f.scan || f.Scan_ID || f.scanId)
    .filter((id, index, self) => id && self.indexOf(id) === index);

  console.log("=== UNIQUE SCANS ===", uniqueScans);

  // Extract unique URLs - trying ALL possible field names
  const uniqueUrls = findings
    .map(f => f.target || f.url || FTarget || FUrl)
    .filter((url, index, self) => url && self.indexOf(url) === index);

  console.log("=== UNIQUE URLs ===", uniqueUrls);

  const filteredFindings = findings.filter(f => {
    // Get the correct field values (trying all possible names)
    const scanValue = f.scan_id || f.scan || f.Scan_ID || f.scanId;
    const urlValue = f.target || f.url || f.Target || f.url;

    console.log("=== FILTERING ===", {
      finding: f.id,
      scanValue,
      urlValue,
      severityFilter,
      scanFilter,
      urlFilter
    });

    // Severity filter
    if (severityFilter !== "All" && f.severity !== severityFilter) {
      return false;
    }

    // Scan ID filter
    if (scanFilter && scanValue !== scanFilter) {
      return false;
    }

    // URL filter
    if (urlFilter && urlValue !== urlFilter) {
      return false;
    }

    // Search text filter
    if (searchText) {
      const searchLower = searchText.toLowerCase();
      if (
        !f.name.toLowerCase().includes(searchLower) &&
        !f.id.toLowerCase().includes(searchLower)
      ) {
        return false;
      }
    }

    return true;
  });

  console.log("=== FILTERED FINDINGS COUNT ===", filteredFindings.length);

  const getSeverityGradient = (severity) => {
    switch (severity) {
      case "Critical":
        return "linear-gradient(90deg, #ef4444, #dc2626)";
      case "High":
        return "linear-gradient(90deg, #f97316, #ea580c)";
      case "Medium":
        return "linear-gradient(90deg, #eab308, #ca8a04)";
      case "Low":
        return "linear-gradient(90deg, #22c55e, #16a34a)";
      default:
        return "linear-gradient(90deg, #64748b, #475569)";
    }
  };

  const pageStyle = {
    maxWidth: "1000px",
    margin: "0 auto"
  };

  const headerStyle = {
    background: "linear-gradient(90deg, #60a5fa, #a78bfa)",
    backgroundClip: "text",
    WebkitBackgroundClip: "text",
    color: "transparent",
    fontWeight: "800",
    fontSize: "24px",
    marginBottom: "18px"
  };

  const filterRowStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "12px",
    marginBottom: "18px"
  };

  const filterStyle = {
    padding: "8px 12px",
    borderRadius: "6px",
    background: "linear-gradient(180deg, #1e293b, #0f172a)",
    color: "#e5e7eb",
    border: "1px solid rgba(148, 163, 184, 0.2)",
    fontSize: "12px",
    fontWeight: "600",
    cursor: "pointer",
    outline: "none"
  };

  const inputStyle = {
    padding: "8px 12px",
    borderRadius: "6px",
    background: "linear-gradient(180deg, #1e293b, #0f172a)",
    color: "#e5e7eb",
    border: "1px solid rgba(148, 163, 184, 0.2)",
    fontSize: "12px",
    outline: "none",
    width: "100%"
  };

  const tableStyle = {
    width: "100%",
    background: "linear-gradient(180deg, #1e293b, #0b1221)",
    borderRadius: "10px",
    border: "1px solid rgba(148, 163, 184, 0.2)",
    boxShadow: "0 8px 20px rgba(0,0,0,0.3)",
    overflow: "hidden",
    fontSize: "12px"
  };

  const thStyle = {
    padding: "10px 12px",
    background: "linear-gradient(90deg, #2563eb, #7c3aed)",
    color: "white",
    fontWeight: "700",
    textAlign: "left",
    fontSize: "12px"
  };

  const tdStyle = {
    padding: "8px 12px",
    borderBottom: "1px solid rgba(148, 163, 184, 0.12)",
    color: "#e4e9f2"
  };

  return (
    <Layout>
      <div style={pageStyle}>
        <h1 style={headerStyle}>
          🔍 Security Findings
        </h1>

        {/* DEBUG SECTION - Remove this after fixing */}
        <div style={{ 
          background: "#1e293b", 
          padding: "12px", 
          borderRadius: "8px",
          marginBottom: "18px",
          fontSize: "11px",
          color: "#94a3b8"
        }}>
          <strong>🔧 DEBUG INFO:</strong>
          <div style={{ marginTop: "8px" }}>
            <div>Total findings: {findings.length}</div>
            <div>Unique scans: {uniqueScans.join(", ")}</div>
            <div>Unique URLs: {uniqueUrls.join(", ")}</div>
            {debugData && (
              <div style={{ marginTop: "8px", color: "#60a5fa" }}>
                <strong>First finding keys:</strong> {Object.keys(debugData).join(", ")}
              </div>
            )}
          </div>
        </div>

        {/* Filter Row */}
        <div style={filterRowStyle}>
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            style={filterStyle}
          >
            <option value="All">All Severities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>

          <select
            value={scanFilter}
            onChange={(e) => setScanFilter(e.target.value)}
            style={filterStyle}
          >
            <option value="">All Scans</option>
            {uniqueScans.map((scanId) => (
              <option key={scanId} value={scanId}>
                Scan {scanId}
              </option>
            ))}
          </select>

          <select
            value={urlFilter}
            onChange={(e) => setUrlFilter(e.target.value)}
            style={filterStyle}
          >
            <option value="">All URLs</option>
            {uniqueUrls.map((url) => (
              <option key={url} value={url}>
                {url}
              </option>
            ))}
          </select>

          <input
            type="text"
            placeholder="Search by name or ID..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={inputStyle}
          />
        </div>

        <p style={{ color: "#94a3b8", marginBottom: "12px", fontSize: "12px" }}>
          Showing <strong style={{ color: "#60a5fa" }}>{filteredFindings.length}</strong> findings
        </p>

        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>ID</th>
              <th style={thStyle}>Name</th>
              <th style={thStyle}>Severity</th>
              <th style={thStyle}>Category</th>
              <th style={thStyle}>Scanner</th>
              <th style={thStyle}>Scan</th>
              <th style={thStyle}>URL</th>
              <th style={thStyle}>Risk</th>
            </tr>
          </thead>
          <tbody>
            {filteredFindings.map((finding) => {
              const scanValue = finding.scan_id || finding.scan;
              const urlValue = finding.target || finding.url;
              
              return (
                <tr
                  key={finding.id}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = "rgba(37, 99, 235, 0.1)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = "transparent";
                  }}
                >
                  <td style={{ ...tdStyle, fontWeight: "600" }}>{finding.id}</td>
                  <td style={tdStyle}>{finding.name}</td>
                  <td style={tdStyle}>
                    <span
                      style={{
                        background: getSeverityGradient(finding.severity),
                        padding: "4px 10px",
                        borderRadius: "6px",
                        fontWeight: "600",
                        fontSize: "11px"
                      }}
                    >
                      {finding.severity}
                    </span>
                  </td>
                  <td style={tdStyle}>{finding.category}</td>
                  <td style={tdStyle}>{finding.scanner}</td>
                  <td style={{ ...tdStyle, fontWeight: "600", color: "#60a5fa" }}>
                    {scanValue}
                  </td>
                  <td style={{ ...tdStyle, color: "#a78bfa" }}>{urlValue}</td>
                  <td style={tdStyle}>{finding.risk_score}</td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {filteredFindings.length === 0 && (
          <p style={{ textAlign: "center", color: "#94a3b8", marginTop: "30px", fontSize: "12px" }}>
            🔎 No findings match your filters
          </p>
        )}
      </div>
    </Layout>
  );
}

export default Findings;