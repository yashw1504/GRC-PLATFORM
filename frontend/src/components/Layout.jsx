import { useEffect } from "react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function Layout({ children }) {
  useEffect(() => {
    document.body.style.background = "linear-gradient(180deg, #0b1221, #1e293b)";
    document.body.style.margin = "0";
  }, []);

  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background: "linear-gradient(180deg, #0b1221, #1e293b)",
        fontFamily: "Inter, Arial, sans-serif"
      }}
    >
      <Sidebar />

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column"
        }}
      >
        <Navbar />

        <main
          style={{
            flex: 1,
            padding: "30px",
            color: "#e5e7eb",
            overflow: "auto"
          }}
        >
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;