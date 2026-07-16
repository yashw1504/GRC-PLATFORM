import { useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";
import ScoreCard from "../components/ScoreCard";

const pageStyle = {
  maxWidth: "1200px",
  margin: "0 auto",
  padding: "24px",
  background: "#f8fafc",
  minHeight: "100vh",
  borderRadius: "16px",
};

const headerStyle = {
  color: "#1f2937",
  fontWeight: "800",
  fontSize: "32px",
  marginBottom: "32px",
  letterSpacing: "0.5px",
  textAlign: "center",
};

const loadingStyle = {
  color: "#374151",
  textAlign: "center",
  padding: "40px 0",
};

const gridStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
  gap: "25px",
  marginBottom: "32px",
};

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    API.get("/dashboard")
      .then((res) => {
        setData(res.data);
      })
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <Layout>
        <div style={pageStyle}>
          <h2 style={loadingStyle}>Loading...</h2>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div style={pageStyle}>
        <h1 style={headerStyle}>Security Dashboard</h1>

        <div style={gridStyle}>
          <ScoreCard
            title="Total Scans"
            value={data.total_scans}
            icon="🔍"
            gradient="linear-gradient(90deg, #2563eb, #7c3aed)"
          />
          <ScoreCard
            title="Total Findings"
            value={data.total_findings}
            icon="🔎"
            gradient="linear-gradient(90deg, #10b981, #059669)"
          />
          <ScoreCard
            title="Critical"
            value={data.critical}
            icon="🚨"
            gradient="linear-gradient(90deg, #ef4444, #dc2626)"
          />
          <ScoreCard
            title="High"
            value={data.high}
            icon="⚠️"
            gradient="linear-gradient(90deg, #f59e0b, #d97706)"
          />
        </div>
      </div>
    </Layout>
  );
}

export default Dashboard;