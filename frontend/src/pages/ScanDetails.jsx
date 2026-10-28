import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../services/api";
import Layout from "../components/Layout";

function ScanDetails() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [reports, setReports] = useState([]);
  const [reportsLoading, setReportsLoading] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");

    API.get(`/scans/${id}`)
      .then((response) => {
        if (!response.data?.scan) {
          throw new Error("This scan record was not found.");
        }
        if (active) setData(response.data);
      })
      .catch((requestError) => {
        if (active) {
          setError(
            requestError.response?.data?.detail ||
            requestError.message ||
            "Could not load this scan."
          );
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    API.get(`/reports/${id}`)
      .then((response) => {
        if (active) setReports(response.data.map((report) => report.type));
      })
      .catch(() => {
        if (active) setReports([]);
      })
      .finally(() => {
        if (active) setReportsLoading(false);
      });

    return () => {
      active = false;
    };
  }, [id]);

  if (loading) {
    return (
      <Layout>
        <h2>Loading...</h2>
      </Layout>
    );
  }

  if (error || !data) {
    return (
      <Layout>
        <div role="alert" style={{ color: "#fca5a5", padding: "24px" }}>
          <h2>Could not load scan details</h2>
          <p>{error || "This scan record was not found."}</p>
          <button type="button" onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      </Layout>
    );
  }

  // Extract a clean URL slug from target (e.g., "example.com" from "https://example.com")
  const getUrlSlug = (target) => {
    if (!target) return id;
    return target
      .replace("https://", "")
      .replace("http://", "")
      .split("/")[0]
      .replace(/[^a-zA-Z0-9.-]/g, "-");
  };

  const urlSlug = getUrlSlug(data.scan.target);

  const cardStyle = {
    background: "linear-gradient(180deg, #1e293b, #0f172a)",
    borderRadius: "16px",
    padding: "24px",
    boxShadow: "0 12px 40px rgba(0,0,0,0.45)",
    border: "1px solid rgba(148, 163, 184, 0.2)",
    marginBottom: "24px"
  };

  const gradientText = {
    background: "linear-gradient(90deg, #60a5fa, #a78bfa)",
    backgroundClip: "text",
    WebkitBackgroundClip: "text",
    color: "transparent",
    fontWeight: "800",
    letterSpacing: "0.5px"
  };

  const tableStyle = {
    width: "100%",
    background: "linear-gradient(180deg, #1e293b, #0b1221)",
    borderRadius: "12px",
    border: "1px solid rgba(148, 163, 184, 0.2)",
    boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
    overflow: "hidden"
  };

  const thStyle = {
    padding: "14px 16px",
    background: "linear-gradient(90deg, #2563eb, #7c3aed)",
    color: "white",
    fontWeight: "700",
    textAlign: "left",
    fontSize: "14px"
  };

  const tdStyle = {
    padding: "12px 16px",
    borderBottom: "1px solid rgba(148, 163, 184, 0.15)",
    color: "#e5e7eb"
  };

  return (
    <Layout>
      <div
        style={{
          maxWidth: "1000px",
          margin: "0 auto",
          padding: "20px"
        }}
      >
        <h1 style={{ ...gradientText, fontSize: "32px", marginBottom: "24px" }}>
          ✨ Scan Details
        </h1>

        <div style={cardStyle}>
          <h3 style={{ color: "#60a5fa", marginBottom: "12px", fontSize: "18px" }}>
            🎯 Target: {data.scan.target}
          </h3>
          <h3 style={{ color: "#a78bfa", marginBottom: "12px", fontSize: "18px" }}>
            📊 Score: {data.scan.overall_score}
          </h3>
          <h3 style={{ color: "#94a3b8", fontSize: "18px" }}>
            📅 Date: {data.scan.scan_date}
          </h3>
        </div>

        <div style={cardStyle}>
          <h2 style={{ color: "#60a5fa", marginBottom: "16px", fontSize: "22px" }}>
            🛡️ Compliance Scores
          </h2>

          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={thStyle}>Framework</th>
                <th style={thStyle}>Score</th>
              </tr>
            </thead>
            <tbody>
              {(data.compliance || []).map((item, index) => (
                <tr key={index}>
                  <td style={{ ...tdStyle, fontWeight: "600" }}>{item.framework}</td>
                  <td style={tdStyle}>{item.score == null ? "Not assessed" : `${item.score}%`}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div style={cardStyle}>
          <h2 style={{ color: "#60a5fa", marginBottom: "16px", fontSize: "22px" }}>
            📑 Reports
          </h2>

          <div
            style={{
              display: "flex",
              gap: "16px",
              flexWrap: "wrap"
            }}
          >
            {reports.includes("json") && <a
              href={`/api/download/${id}/json`}
              style={{
                padding: "10px 18px",
                background: "linear-gradient(90deg, #2563eb, #7c3aed)",
                color: "white",
                borderRadius: "8px",
                textDecoration: "none",
                fontWeight: "600",
                boxShadow: "0 6px 16px rgba(37, 99, 235, 0.35)"
              }}
            >
              📄 Download JSON
            </a>}

            {reports.includes("html") && <a
              href={`/api/download/${id}/html`}
              style={{
                padding: "10px 18px",
                background: "linear-gradient(90deg, #1fe4f5, #2563eb)",
                color: "#0f172a",
                borderRadius: "8px",
                textDecoration: "none",
                fontWeight: "600",
                boxShadow: "0 6px 16px rgba(37, 99, 235, 0.25)"
              }}
            >
              🌐 Download HTML
            </a>}

            {reports.includes("executive") && <a
              href={`/api/download/${id}/executive`}
              style={{
                padding: "10px 18px",
                background: "linear-gradient(90deg, #fbbf24, #f59e0b)",
                color: "#0f172a",
                borderRadius: "8px",
                textDecoration: "none",
                fontWeight: "600",
                boxShadow: "0 6px 16px rgba(251, 191, 36, 0.35)"
              }}
            >
              📊 Download Executive
            </a>}
            {reports.includes("excel") && <a
              href={`/api/download/${id}/excel`}
              style={{
                padding: "10px 18px",
                background: "linear-gradient(90deg, #22c55e, #15803d)",
                color: "white",
                borderRadius: "8px",
                textDecoration: "none",
                fontWeight: "600",
                boxShadow: "0 6px 16px rgba(34, 197, 94, 0.25)"
              }}
            >
              Download Excel
            </a>}
            {!reportsLoading && reports.length === 0 && (
              <p role="status" style={{ color: "#cbd5e1" }}>
                No reports were generated for this scan. It may have failed before report generation.
              </p>
            )}
          </div>
        </div>

        <div style={cardStyle}>
          <h2 style={{ color: "#60a5fa", marginBottom: "16px", fontSize: "22px" }}>
            🔍 Findings
          </h2>

          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Name</th>
                <th style={thStyle}>Severity</th>
                <th style={thStyle}>Risk Score</th>
              </tr>
            </thead>
            <tbody>
              {(data.findings || []).map((finding) => (
                <tr key={finding.id}>
                  <td style={{ ...tdStyle, fontWeight: "600" }}>{finding.id}</td>
                  <td style={tdStyle}>{finding.name}</td>
                  <td style={tdStyle}>{finding.severity}</td>
                  <td style={tdStyle}>{finding.risk_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}

export default ScanDetails;
