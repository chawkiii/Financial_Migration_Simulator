// frontend/src/components/ProjectionChart.jsx
import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend
} from "recharts";

export default function ProjectionChart({ projections }) {

  if (!projections || projections.length === 0) return null;

  return (
    <div className="projection-chart">

      <h3>Monthly Balance Projection</h3>

      <div className="chart-container">

        <ResponsiveContainer width="100%" height="100%">

          <LineChart data={projections}>

            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />

            <XAxis
              dataKey="month"
              stroke="#cbd5f5"
            />

            <YAxis
              stroke="#cbd5f5"
            />

            <Tooltip />

            <Legend />

            <Line
              type="monotone"
              dataKey="start"
              stroke="#a78bfa"
              strokeWidth={2}
              dot={false}
              name="Starting Balance"
            />

            <Line
              type="monotone"
              dataKey="end"
              stroke="#4ade80"
              strokeWidth={2}
              dot={false}
              name="Ending Balance"
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}
