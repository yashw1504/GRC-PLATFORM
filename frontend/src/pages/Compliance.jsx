import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import API from "../services/api";
import Layout from "../components/Layout";

function Compliance() {

  const [scans, setScans] =
    useState([]);

  useEffect(() => {

    API.get("/scans")
      .then((response) => {

        setScans(
          response.data
        );

      });

  }, []);

  return (

    <Layout>

      <h1>
        Compliance Dashboard
      </h1>

      <table
        style={{
          width: "100%",
          background: "#07295c",
          color: "white"
        }}
      >

        <thead>

          <tr>

            <th>ID</th>

            <th>Target</th>

            <th>Score</th>

            <th>Action</th>

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

                    <Link
                      to={`/compliance/${scan.id}`}
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

export default Compliance;