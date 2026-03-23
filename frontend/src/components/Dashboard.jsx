import { useState } from "react";
import { useSimulation } from "../context/SimulationContext.jsx";
import { runSimulation } from "../services/api.js";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const { inputs, updateInputs, result, setResult, loading, setLoading, resetSimulation } = useSimulation();
  const [scenarioIncome, setScenarioIncome] = useState(0);
  const [activeTab, setActiveTab] = useState("overview");

  const handleChange = (e) => {
    const { name, value } = e.target;
    updateInputs({ [name]: Number(value) || value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = { ...inputs, monthly_income: inputs.monthly_income * (1 + scenarioIncome / 100) };
      const res = await runSimulation(data);
      setResult(res);
    } catch {
      alert("Erreur lors de la simulation !");
    } finally {
      setLoading(false);
    }
  };

  const tabs = ["overview", "risk", "score", "insights", "provinces"];

  return (
    <div style={{ padding: "2rem", fontFamily: "Inter, sans-serif" }}>
      <h1>CapAhead Financial Dashboard</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <div>
            <label>Initial Savings:</label>
            <input type="number" name="initial_savings" value={inputs.initial_savings} onChange={handleChange} />
          </div>
          <div>
            <label>Monthly Income:</label>
            <input type="number" name="monthly_income" value={inputs.monthly_income} onChange={handleChange} />
          </div>
          <div>
            <label>Monthly Expenses:</label>
            <input type="number" name="monthly_expenses" value={inputs.monthly_expenses} onChange={handleChange} />
          </div>
          <div>
            <label>Province:</label>
            <select name="province" value={inputs.province} onChange={handleChange}>
              <option value="alberta">Alberta</option>
              <option value="ontario">Ontario</option>
              <option value="quebec">Quebec</option>
            </select>
          </div>
        </div>

        <div style={{ margin: "1rem 0" }}>
          <label>Scenario Income Increase: {scenarioIncome}%</label>
          <input type="range" min="0" max="50" step="1" value={scenarioIncome} onChange={(e) => setScenarioIncome(Number(e.target.value))} />
        </div>

        <div style={{ marginTop: "1rem" }}>
          <button type="submit" disabled={loading}>{loading ? "Running..." : "Run Simulation"}</button>
          <button type="button" onClick={resetSimulation} style={{ marginLeft: "1rem" }}>Reset</button>
        </div>
      </form>

      {loading && <p>Running simulation… 🚀</p>}

      {result && (
        <>
          <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
            {tabs.map(tab => (
              <button
                key={tab}
                style={{
                  padding: "0.5rem 1rem",
                  backgroundColor: activeTab === tab ? "#4F46E5" : "#eee",
                  color: activeTab === tab ? "#fff" : "#000",
                  border: "none",
                  cursor: "pointer"
                }}
                onClick={() => setActiveTab(tab)}
              >
                {tab.toUpperCase()}
              </button>
            ))}
          </div>

          {activeTab === "overview" && (
            <div>
              <h2>Overview</h2>
              <div style={{ display: "flex", gap: "1rem" }}>
                <div style={{ padding: "1rem", border: "1px solid #ccc" }}>
                  <strong>Final Balance</strong>
                  <p>${result.summary.final_balance?.toLocaleString() || 0}</p>
                </div>
                <div style={{ padding: "1rem", border: "1px solid #ccc" }}>
                  <strong>Cashflow</strong>
                  <p>${result.summary.monthly_cashflow?.toLocaleString() || 0}</p>
                </div>
                <div style={{ padding: "1rem", border: "1px solid #ccc" }}>
                  <strong>Taxes</strong>
                  <p>${result.tax?.total?.toLocaleString() || 0}</p>
                </div>
              </div>

              {result.summary.monthly_balance && (
                <div style={{ marginTop: "2rem", height: "300px" }}>
                  <h3>Balance Over Time</h3>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={result.summary.monthly_balance}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="balance" stroke="#4F46E5" activeDot={{ r: 8 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>
          )}

          {activeTab === "risk" && (
            <div>
              <h2>Risk Assessment</h2>
              <p><strong>Risk Level:</strong> {result.risk}</p>
            </div>
          )}

          {activeTab === "score" && (
            <div>
              <h2>Score</h2>
              <p>{result.score} / 100</p>
            </div>
          )}

          {activeTab === "insights" && (
            <div>
              <h2>Insights</h2>
              <pre>{JSON.stringify(result.insights || {}, null, 2)}</pre>
            </div>
          )}

          {activeTab === "provinces" && (
            <div>
              <h2>Province Ranking</h2>
              <table border="1" cellPadding="5">
                <thead>
                  <tr>
                    <th>Province</th>
                    <th>Score</th>
                    <th>Risk</th>
                    <th>Final Balance</th>
                  </tr>
                </thead>
                <tbody>
                  {result.strategy?.province_ranking?.map((prov, idx) => (
                    <tr key={idx}>
                      <td>{prov.name}</td>
                      <td>{prov.score}</td>
                      <td>{prov.risk}</td>
                      <td>${prov.final_balance?.toLocaleString() || 0}</td>
                    </tr>
                  )) || (
                    <tr>
                      <td colSpan="4">No province ranking available</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}