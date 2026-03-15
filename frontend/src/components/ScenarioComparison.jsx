// frontend/src/components/ScenarioComparison.jsx

import { useState } from "react";
import api from "../services/api";

export default function ScenarioComparison({ baseInput }) {

  const [results, setResults] = useState(null);

  const runComparison = async () => {

    const scenarios = [

      baseInput,

      { ...baseInput, monthly_income: baseInput.monthly_income + 500 },

      { ...baseInput, monthly_income: baseInput.monthly_income + 1000 }

    ];

    const res = await api.post("/compare", {
      scenarios
    });

    setResults(res.data.scenarios);
  };

  return (

    <div>

      <h3>Scenario Comparison</h3>

      <button onClick={runComparison}>
        Compare Salary Scenarios
      </button>

      {results && (

        <table>

          <thead>
            <tr>
              <th>Scenario</th>
              <th>Final Balance</th>
              <th>Score</th>
              <th>Success</th>
              <th>Risk</th>
            </tr>
          </thead>

          <tbody>

            {results.map((r, i) => (

              <tr key={i}>
                <td>{r.name}</td>
                <td>{r.final_balance}</td>
                <td>{r.financial_score}</td>
                <td>{r.success_probability}%</td>
                <td>{r.risk_level}</td>
              </tr>

            ))}

          </tbody>

        </table>

      )}

    </div>

  );

}