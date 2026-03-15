// frontend/src/components/SimulationHistory.jsx

import { useEffect, useState } from "react";
import api from "../services/api";

export default function SimulationHistory() {

  const [history, setHistory] = useState([]);

  useEffect(() => {

    const loadHistory = async () => {

      const res = await api.get("/history");

      setHistory(res.data.history);
    };

    loadHistory();

  }, []);

  return (

    <div>

      <h3>Previous Simulations</h3>

      <table>

        <thead>
          <tr>
            <th>Date</th>
            <th>Province</th>
            <th>Final Balance</th>
            <th>Score</th>
            <th>Success</th>
          </tr>
        </thead>

        <tbody>

          {history.map((s) => (

            <tr key={s.id}>
              <td>{new Date(s.created_at).toLocaleDateString()}</td>
              <td>{s.province}</td>
              <td>{s.results.final_balance}</td>
              <td>{s.results.score}</td>
              <td>{s.results.success_probability}%</td>
            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}