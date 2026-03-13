// frontend/src/components/ResultsPanel.jsx
import React from "react";

export default function ResultsPanel({ result }) {

  return (
    <div>

      <h2>Simulation Results</h2>

      <p>Final Balance: {result.simulation.final_balance}</p>

      <p>Financial Score: {result.analysis.financial_score}</p>

      <p>
        Success Probability:
        {result.success_probability.success_probability}%
      </p>

      <h3>Insights</h3>

      <ul>
        {result.analysis.insights.map((i, index) => (
          <li key={index}>{i}</li>
        ))}
      </ul>

      <h3>Monte Carlo Analysis</h3>

      <p>Success Rate: {result.monte_carlo.success_rate}%</p>
      <p>Failure Rate: {result.monte_carlo.failure_rate}%</p>
      <p>Average Final Balance: {result.monte_carlo.average_final_balance}</p>
      <p>Worst Case Balance: {result.monte_carlo.worst_balance}</p>

      <h3>Risk Analysis</h3>

      <p>Risk Level: {result.risk.risk_level}</p>
      <p>Risk Score: {result.risk.risk_score}</p>

      <h3>Strategy</h3>

      <ul>
        {result.strategy.map((s, index) => (
          <li key={index}>{s}</li>
        ))}
      </ul>

    </div>
  );
}