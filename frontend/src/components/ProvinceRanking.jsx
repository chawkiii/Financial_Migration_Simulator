// frontend/src/components/ProvinceRanking.jsx

import { useState } from "react";
import api from "../services/api";

export default function ProvinceRanking({ input }) {

  const [rankings, setRankings] = useState(null);

  const runRanking = async () => {

    const res = await api.post("/province-ranking", input);

    setRankings(res.data.rankings);
  };

  return (

    <div>

      <h3>Best Provinces for Your Situation</h3>

      <button onClick={runRanking}>
        Find Best Province
      </button>

      {rankings && (

        <table>

          <thead>
            <tr>
              <th>Province</th>
              <th>Score</th>
              <th>Risk</th>
              <th>Final Balance</th>
            </tr>
          </thead>

          <tbody>

            {rankings.map((p, i) => (

              <tr key={i}>
                <td>{p.province}</td>
                <td>{p.score}</td>
                <td>{p.risk_level}</td>
                <td>{p.final_balance}</td>
              </tr>

            ))}

          </tbody>

        </table>

      )}

    </div>

  );

}