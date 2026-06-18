import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import RunScan from "./pages/RunScan";
import Findings from "./pages/Findings";
import Compliance from "./pages/Compliance";
import Scans from "./pages/Scans";
import ScanDetails from "./pages/ScanDetails";
import ComplianceDetails from "./pages/ComplianceDetails";

function App() {

  return (

    <BrowserRouter>

      <Navbar />

      <div style={{ padding: "20px" }}>

        <Routes>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/scan"
            element={<RunScan />}
          />

          <Route
            path="/findings"
            element={<Findings />}
          />

          <Route
            path="/compliance"
            element={<Compliance />}
          />

          <Route
            path="/scans"
            element={<Scans />}
          />

          <Route
            path="/scans/:id"
            element={
              <ScanDetails />
            }
          />
          <Route
            path="/compliance/:id"
            element={
              <ComplianceDetails />
            }
          />

        </Routes>

      </div>

    </BrowserRouter>

  );

}

export default App;