import { useEffect, useRef, useState } from "react";
import API from "../services/api";

function RunScan() {
  const [targetType, setTargetType] = useState("website");
  const [target, setTarget] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);

  const timerRef = useRef(null);
  const startTimeRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const startTimer = () => {
    startTimeRef.current = Date.now();
    setElapsedTime(0);

    timerRef.current = setInterval(() => {
      setElapsedTime(Math.floor((Date.now() - startTimeRef.current) / 1000));
    }, 1000);
  };

  const stopTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  const runScan = async () => {
    try {
      setLoading(true);
      setResult(null);
      startTimer();

      const response = await API.post("/scan", {
        target: target,
        target_type: targetType
      });

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Scan failed");
    } finally {
      setLoading(false);
      stopTimer();
    }
  };

  const buttonStyle = {
    padding: "12px 20px",
    cursor: loading ? "not-allowed" : "pointer",
    background: loading
      ? "linear-gradient(90deg, #cbd5e1, #94a3b8)"
      : "linear-gradient(90deg, #5e88e2, #9e72eb)",
    color: "white",
    border: "none",
    borderRadius: "12px",
    boxShadow: loading
      ? "none"
      : "0 8px 24px rgba(37, 99, 235, 0.35)",
    transition: "transform 0.2s, box-shadow 0.2s",
    fontWeight: "600"
  };

  const cardStyle = {
    background: "linear-gradient(180deg, #1e293b, #0f172a)",
    borderRadius: "16px",
    padding: "24px",
    boxShadow: "0 12px 40px rgba(0,0,0,0.45)",
    border: "1px solid rgba(148, 163, 184, 0.2)"
  };

  const inputStyle = {
    width: "50%",
    padding: "12px 16px",
    borderRadius: "10px",
    border: "1px solid #334155",
    background: "#16284f",
    color: "white",
    fontSize: "14px",
    outline: "none"
  };

  const labelStyle = {
    color: "#94a3b8",
    fontWeight: "600",
    marginBottom: "6px",
    display: "block"
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "40px 20px",
        background:
          "linear-gradient(180deg, #0b1221, #1e293b)",
        fontFamily: "Inter, Arial, sans-serif",
        color: "#e5e7eb"
      }}
    >
      <div style={{ maxWidth: "900px", margin: "0 auto" }}>
        <div style={cardStyle}>
          <h1
            style={{
              textAlign: "center",
              marginBottom: "24px",
              fontSize: "32px",
              fontWeight: "800",
              background: "linear-gradient(90deg, #60a5fa, #a78bfa)",
              backgroundClip: "text",
              WebkitBackgroundClip: "text",
              color: "transparent",
              letterSpacing: "0.5px"
            }}
          >
            Scan Center
          </h1>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(5, 1fr)",
              gap: "12px",
              marginBottom: "28px"
            }}
          >
            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>🌐 Website</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>🔗 API</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>🖥 Network</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1fe4f5, #2563eb)",
              color: "#0f172a",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(37, 99, 235, 0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>☁ AWS</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1fe4f5, #2563eb)",
              color: "#0f172a",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(37, 99, 235, 0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>☁ Azure</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>☁ GCP</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>📦 Container</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>☸ Kubernetes</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>📜 Terraform</button>

            <button type="button" style={{
              padding: "12px 10px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(90deg, #1e293b, #0f172a)",
              color: "#94a3b8",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              transition: "transform 0.2s, box-shadow 0.2s",
              fontWeight: "600"
            }}>📱 APK</button>
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={labelStyle}>Target Type</label>
            <select
              value={targetType}
              onChange={(e) => setTargetType(e.target.value)}
              style={{
                ...inputStyle,
                cursor: "pointer"
              }}
            >
              <option value="website">Website</option>
              <option value="ip">IP Address</option>
              <option value="api">API Endpoint</option>
              <option value="source">Source Code</option>
              <option value="container">Docker Image</option>
              <option value="kubernetes">Kubernetes YAML</option>
              <option value="terraform">Terraform</option>
              <option value="apk">APK File</option>
              <option value="aws">AWS Account</option>
              <option value="azure">Azure Tenant</option>
              <option value="gcp">GCP Project</option>
            </select>
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={labelStyle}>Target</label>
            <input
              type="text"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder="Enter URL, IP, Path..."
              style={inputStyle}
            />
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={labelStyle}>Upload File</label>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              style={{
                color: "#eceff1"
              }}
            />
          </div>

          <button
            onClick={runScan}
            disabled={loading}
            style={buttonStyle}
          >
            {loading ? `Scanning... ${elapsedTime}s` : "Run Scan"}
          </button>

          {loading && (
            <div
              style={{
                marginTop: "20px",
                padding: "16px",
                background: "linear-gradient(90deg, #224e95, #203d80)",
                border: "1px solid rgba(37, 99, 235, 0.4)",
                borderRadius: "12px",
                boxShadow: "0 8px 24px rgba(37, 99, 235, 0.25)"
              }}
            >
              <strong style={{ color: "#60a5fa", fontSize: "16px" }}>
                🚀 Scan in progress
              </strong>
              <div style={{ marginTop: "8px", color: "#94a3b8" }}>
                Elapsed time: <strong style={{ color: "#a78bfa" }}>{elapsedTime}s</strong>
              </div>
            </div>
          )}

          {result && (
            <div
              style={{
                marginTop: "30px",
                background: "linear-gradient(180deg, #1e293b, #0b1221)",
                border: "1px solid rgba(148, 163, 184, 0.25)",
                borderRadius: "16px",
                padding: "24px",
                boxShadow: "0 12px 40px rgba(0,0,0,0.4)"
              }}
            >
              <h2
                style={{
                  marginBottom: "16px",
                  fontSize: "22px",
                  fontWeight: "700",
                  color: "#3d79c3"
                }}
              >
                ✨ Scan Result
              </h2>

              <p>
                <strong style={{ color: "#e9e7f0" }}>Target:</strong> {result.target}
              </p>
              <p>
                <strong style={{ color: "#a78bfa" }}>Overall Score:</strong> {result.overall_score}
              </p>
              <p>
                <strong style={{ color: "#a78bfa" }}>Findings:</strong> {result.findings?.length ?? 0}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default RunScan;