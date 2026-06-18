import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import API from "../services/api";
import Layout from "../components/Layout";

function ComplianceDetails() {

  const { id } = useParams();

  const [scores, setScores] =
    useState([]);

  useEffect(() => {

    API.get(
      `/compliance/${id}`
    )
    .then((response) => {

      setScores(
        response.data
      );

    })
    .catch(console.error);

  }, [id]);

  return (

    <Layout>

      <h1>
        Compliance Dashboard
      </h1>

      <h3>
        Scan ID: {id}
      </h3>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
          marginTop: "20px"
        }}
      >

        {
          scores.map(
            score => (

              <div
                key={
                  score.framework
                }
                style={{
                  background:
                    "#729ada",
                  padding:
                    "20px",
                  borderRadius:
                    "12px"
                }}
              >

                <h2>
                  {
                    score.framework
                  }
                </h2>

                <h1>
                  {
                    score.score
                  }%
                </h1>

              </div>

            )
          )
        }

      </div>

    </Layout>

  );

}

export default ComplianceDetails;