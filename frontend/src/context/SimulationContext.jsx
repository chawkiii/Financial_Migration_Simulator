// frontend/src/context/SimulationContext.jsx

import { createContext, useContext, useState } from "react";

const SimulationContext = createContext();
export const useSimulation = () => useContext(SimulationContext);

export const SimulationProvider = ({ children }) => {
  const [inputs, setInputs] = useState({
    initial_savings: 0,
    monthly_income: 0,
    monthly_expenses: 0,
    months: 12,
    savings_goal: 0,
    one_time_cost: 0,
    months_without_income: 0,
    province: "alberta",
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const updateInputs = (newInputs) => setInputs((prev) => ({ ...prev, ...newInputs }));
  const resetSimulation = () => {
    setInputs({
      initial_savings: 0,
      monthly_income: 0,
      monthly_expenses: 0,
      months: 12,
      savings_goal: 0,
      one_time_cost: 0,
      months_without_income: 0,
      province: "alberta",
    });
    setResult(null);
  };

  return (
    <SimulationContext.Provider
      value={{ inputs, updateInputs, result, setResult, loading, setLoading, resetSimulation }}
    >
      {children}
    </SimulationContext.Provider>
  );
};