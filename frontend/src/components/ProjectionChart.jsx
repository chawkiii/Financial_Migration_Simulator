// frontend/src/components/ProjectionChart.jsx
import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function ProjectionChart({ projections }) {
  if (!projections || projections.length === 0) return null;

  return (
    <div className="projection-chart" style={{ width: "100%", height: 300 }}>
      <h3>Monthly Projections</h3>
      <ResponsiveContainer>
        <LineChart data={projections}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="start" stroke="#8884d8" name="Starting Balance" />
          <Line type="monotone" dataKey="end" stroke="#82ca9d" name="Ending Balance" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}