// frontend/src/pages/SimulatorPage.jsx

import { useState } from "react";
import SimulationForm from "../components/SimulationForm";
import ResultsPanel from "../components/ResultsPanel";
import ProjectionChart from "../components/ProjectionChart";
import { runSimulation } from "../services/api";

export default function SimulatorPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRun = async (data) => {
    setLoading(true);
    try {
      const response = await runSimulation(data);
      console.log(response); // Debug log to check the response structure
      setResult(response);
    } catch (error) {
      console.error("Simulation failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Canada Financial Engine</h1>

      <SimulationForm onRun={handleRun} />
      {loading && <p>Running simulation...</p>}

      {result && (
        <>
          <ResultsPanel result={result} />
          <ProjectionChart projections={result.simulation.monthly_projections} />
        </>
      )}
    </div>
  );
}