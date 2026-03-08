# financial_simulator/api/main.py
from fastapi import FastAPI, HTTPException
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
    expenses: dict[str, float] | None = None


@app.post("/simulate")
def run_simulation(data: SimulationInput):

    try:
        inputs = FinancialInputs(**data.model_dump())

        engine = ProjectionEngine(inputs)
        result = engine.simulate(force=True)

        scorer = FinancialScorer(inputs)
        score = scorer.calculate(result)

        return {
            "final_balance": round(result.final_balance, 2),
            "goal_reached_month": result.goal_reached_month,
            "went_negative_during_simulation": result.went_negative_during_simulation,
            "diagnosis": engine.generate_diagnosis(score),
            "score": round(score, 2),

            "monthly_projections": [
                {
                    "month": p.month_number,
                    "start": round(p.starting_balance, 2),
                    "end": round(p.ending_balance, 2),
                    "cashflow": round(p.net_cashflow, 2),
                }
                for p in result.projections
            ],
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))