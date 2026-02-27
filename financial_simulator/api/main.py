# financial_simulator/api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.core.scoring import FinancialScorer

app = FastAPI(title="Financial Migration Simulator API")

class SimulationInput(BaseModel):
    initial_savings: float
    one_time_cost: float
    monthly_income: float
    monthly_expenses: float
    months: int
    savings_goal: float
    months_without_income: int = 0

@app.post("/simulate")
def run_simulation(data: SimulationInput):
    inputs = FinancialInputs(**data.dict())
    engine = ProjectionEngine(inputs)
    result = engine.simulate(force=True)
    scorer = FinancialScorer(inputs)
    score = scorer.calculate(result)
    
    return {
        "final_balance": result.final_balance,
        "goal_reached_month": result.goal_reached_month,
        "went_negative": result.went_negative_during_simulation,
        "diagnosis": engine.generate_diagnosis(score),
        "score": score,
        "monthly_projections": [
            {
                "month": p.month_number,
                "start": p.starting_balance,
                "end": p.ending_balance,
                "cashflow": p.net_cashflow,
            }
            for p in result.projections
        ],
    }