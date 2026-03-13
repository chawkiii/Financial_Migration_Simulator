// frontend/src/components/SimulationForm.jsx

import { useState } from "react";

export default function SimulationForm({ onRun }) {
  const [form, setForm] = useState({
    initial_savings: 20000,
    one_time_cost: 5000,
    monthly_income: 3000,
    monthly_expenses: 2000,
    months: 24,
    savings_goal: 15000,
    months_without_income: 3
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: Number(e.target.value)
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onRun(form);
  };

  return (
    <form onSubmit={handleSubmit}>

      {Object.keys(form).map((key) => (
        <div key={key}>
          <label>{key}</label>
          <input
            type="number"
            name={key}
            value={form[key]}
            onChange={handleChange}
          />
        </div>
      ))}

      <button type="submit">Run Simulation</button>

    </form>
  );
}