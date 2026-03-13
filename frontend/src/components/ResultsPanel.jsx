// frontend/src/components/ResultsPanel.jsx
import React from "react";

export default function ResultsPanel({ result }) {

  const sim = result.simulation;

  return (
    <div className="results">

      <h2>Simulation Results</h2>

      <h3>Financial Outcome</h3>

      <p>Final Balance: {sim.final_balance}</p>

      <p>Goal Reached Month: {sim.goal_reached_month ?? "Not reached"}</p>

      <p>Went Negative: {sim.went_negative ? "Yes" : "No"}</p>

      <p>Insolvent Before Income: {sim.insolvent_before_income ? "Yes" : "No"}</p>

      <p>Maximum Negative Balance: {sim.max_negative_balance}</p>

      <p>Average Monthly Cashflow: {sim.average_cashflow}</p>

      <p>Minimum Financial Cushion (months): {sim.min_cushion}</p>


      <h3>Financial Score</h3>

      <p>Score: {result.analysis.financial_score}</p>

      <p>Interpretation: {result.analysis.interpretation}</p>


      <h3>Success Probability</h3>

      <p>
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
