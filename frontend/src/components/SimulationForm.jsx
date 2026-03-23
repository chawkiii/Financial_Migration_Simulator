// frontend/src/components/SimulationForm.jsx

import { useState } from "react";
import { useSimulation } from "../context/SimulationContext.jsx";
import { runSimulation } from "../services/api.js";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

function ScenarioSlider({ onChange }) {
  return (
    <div style={{ margin: "1rem 0" }}>
      <label>Increase Income: </label>
      <input type="range" min="0" max="50" step="1" onChange={(e) => onChange(Number(e.target.value))} />
      <span> +<b id="slider-value">0</b>%</span>
    </div>
  );
}

export default function SimulationForm() {
  const { inputs, updateInputs, result, setResult, loading, setLoading, resetSimulation } = useSimulation();
  const [scenarioIncome, setScenarioIncome] = useState(0);

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

  return (
    <div style={{ padding: "2rem", fontFamily: "Inter, sans-serif" }}>
      <h1>Simulate your financial future</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <label>Initial Savings:</label>
        <input type="number" name="initial_savings" value={inputs.initial_savings} onChange={handleChange} />
        <label>Monthly Income:</label>
        <input type="number" name="monthly_income" value={inputs.monthly_income} onChange={handleChange} />
        <label>Monthly Expenses:</label>
        <input type="number" name="monthly_expenses" value={inputs.monthly_expenses} onChange={handleChange} />
        <label>Province:</label>
        <select name="province" value={inputs.province} onChange={handleChange}>
          <option value="alberta">Alberta</option>
          <option value="ontario">Ontario</option>
          <option value="quebec">Quebec</option>
        </select>

        <ScenarioSlider onChange={setScenarioIncome} />

        <div style={{ marginTop: "1rem" }}>
          <button type="submit" disabled={loading}>{loading ? "Running..." : "Run Simulation"}</button>
          <button type="button" onClick={resetSimulation} style={{ marginLeft: "1rem" }}>Reset</button>
        </div>
      </form>

      {loading && <p>Running simulation… 🚀</p>}

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Mini Dashboard</h2>
          <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
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
            <div style={{ marginBottom: "2rem", height: "300px" }}>
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
    </div>
  );
}