import { useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";
import { Link } from "react-router-dom";

function Scans() {

  const [scans, setScans] =
    useState([]);

  useEffect(() => {

    API.get("/scans")
      .then((res) => {
        setScans(res.data);
      });

  }, []);

  return (

    <Layout>

      <h1>
        Scan History
      </h1>

      <table
        style={{
          width: "100%",
          background: "#10264a",
          color: "white"
        }}
      >

        <thead>

          <tr>

            <th>ID</th>

            <th>Target</th>

            <th>Risk Score</th>

            <th>Date</th>

            <th>Actions</th>

            <th>Type</th>

          </tr>

        </thead>

        <tbody>

          {
            scans.map(
              scan => (

                <tr
                  key={scan.id}
                >

                  <td>
                    {scan.id}
                  </td>

                  <td>
                    {scan.target}
                  </td>

                  <td>
                    {
                      scan.overall_score
                    }
                  </td>

                  <td>
                    {
                      scan.scan_date
                    }
                  </td>

                  <td>
                    {scan.scan_type}
                  </td>

                  <td>

                  <Link
                      to={`/scans/${scan.id}`}
                  >
                      View
                  </Link>

                  </td>

                </tr>

              )
            )
          }

        </tbody>

      </table>

    </Layout>

  );

}

export default Scans;