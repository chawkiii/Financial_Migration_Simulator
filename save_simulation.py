# save_simulation.py
import json
from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine


inputs = FinancialInputs(
    initial_savings=10000,
    one_time_cost=3500,
    monthly_income=2560,
    monthly_expenses=2200,
    months=12,
    savings_goal=8000,
    months_without_income=1,
)

engine = ProjectionEngine(inputs)
result = engine.simulate()

# Sauvegarde en JSON
with open("simulation_v2_2.json", "w") as f:
    json.dump(result.to_dict(), f, indent=4)

print("JSON saved as simulation_v2_2.json")
