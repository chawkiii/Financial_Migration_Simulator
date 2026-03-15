// frontend/src/components/SimulationForm.jsx

import { useState } from "react";

export default function SimulationForm({ onRun }) {

  const [mode, setMode] = useState("simple");

  const [form, setForm] = useState({
    province: "ontario",
    initial_savings: 11000,
    one_time_cost: 3000,
    monthly_income: 2600,
    monthly_expenses: 2200,
    months: 24,
    savings_goal: 7000,
    months_without_income: 3,
    expenses: {
      rent: 800,
      food: 400,
      transport: 150,
      phone: 100
    }
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm({
      ...form,
      [name]: name === "province" ? value : Number(value)
    });
  };

  const handleExpenseChange = (e) => {
    const { name, value } = e.target;

    setForm({
      ...form,
      expenses: {
        ...form.expenses,
        [name]: Number(value)
      }
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = { ...form };

    if (mode === "simple") {
      payload.expenses = null;
    } else {
      payload.monthly_expenses = 0;
    }

    onRun(payload);
  };

  const Field = ({ label, hint, children }) => (
    <div className="field">
      <label>{label}</label>
      <div className="field-row">
        <div className="field-input">
          {children}
        </div>
        {hint && (
          <div className="field-hint">
            {hint}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <form onSubmit={handleSubmit}>

      <Field
        label="Province"
        hint="🗺 Taxes & cost of living depend on province."
      >
        <select
          name="province"
          value={form.province}
          onChange={handleChange}
        >
          <option value="ontario">Ontario</option>
          <option value="quebec">Quebec</option>
          <option value="alberta">Alberta</option>
          <option value="british_columbia">British Columbia</option>
        </select>
      </Field>

      <h3>Financial Inputs</h3>

      <Field
        label="Initial Savings"
        hint="💰 Money available before arrival."
      >
        <input
          type="number"
          name="initial_savings"
          value={form.initial_savings}
          onChange={handleChange}
        />
      </Field>

      <Field
        label="One-Time Cost"
        hint="✈️ Flights, deposit, furniture, admin fees."
      >
        <input
          type="number"
          name="one_time_cost"
          value={form.one_time_cost}
          onChange={handleChange}
        />
      </Field>

      <Field
        label="Monthly Income"
        hint="💼 Gross income (taxes applied automatically)."
      >
        <input
          type="number"
          name="monthly_income"
          value={form.monthly_income}
          onChange={handleChange}
        />
      </Field>

      <h3>Expenses Mode</h3>

      <div className="radio-group">
        <label>
          <input
            type="radio"
            checked={mode === "simple"}
            onChange={() => setMode("simple")}
          />
          Simple
        </label>

        <label>
          <input
            type="radio"
            checked={mode === "detailed"}
            onChange={() => setMode("detailed")}
          />
          Detailed
        </label>
      </div>

      {mode === "simple" && (
        <Field
          label="Monthly Expenses"
          hint="🏠 Total living expenses."
        >
          <input
            type="number"
            name="monthly_expenses"
            value={form.monthly_expenses}
            onChange={handleChange}
          />
        </Field>
      )}

      {mode === "detailed" && (
        <>
          <Field label="Rent" hint="🏠 Housing cost.">
            <input
              type="number"
              name="rent"
              value={form.expenses.rent}
              onChange={handleExpenseChange}
            />
          </Field>

          <Field label="Food">
            <input
              type="number"
              name="food"
              value={form.expenses.food}
              onChange={handleExpenseChange}
            />
          </Field>

          <Field label="Transport">
            <input
              type="number"
              name="transport"
              value={form.expenses.transport}
              onChange={handleExpenseChange}
            />
          </Field>

          <Field label="Phone">
            <input
              type="number"
              name="phone"
              value={form.expenses.phone}
              onChange={handleExpenseChange}
            />
          </Field>
        </>
      )}

      <Field label="Months to Simulate">
        <input
          type="number"
          name="months"
          value={form.months}
          onChange={handleChange}
        />
      </Field>

      <Field
        label="Savings Goal"
        hint="🎯 Recommended 3–6 months cushion."
      >
        <input
          type="number"
          name="savings_goal"
          value={form.savings_goal}
          onChange={handleChange}
        />
      </Field>

      <Field
        label="Months Without Income"
        hint="⏳ Expected time before finding a job."
      >
        <input
          type="number"
          name="months_without_income"
          value={form.months_without_income}
          onChange={handleChange}
        />
      </Field>

      <button type="submit">
        Run Simulation
      </button>

    </form>
  );
}