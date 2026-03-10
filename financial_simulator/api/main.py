# financial_simulator/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine

from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.analysis.diagnostics import FinancialDiagnostics
from financial_simulator.analysis.readiness import MigrationReadinessIndex

from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.risk.monte_carlo import MonteCarloSimulator

app = FastAPI(
    title="Financial Migration Simulator API",
    version="0.2.6"
)

class SimulationInput(BaseModel):
    initial_savings: float
    one_time_cost: float
    monthly_income: float
    monthly_expenses: float
    months: int
    savings_goal: float
    months_without_income: int = 0
    expenses: dict[str, float] | None = None


@app.get("/")
def root():
    return {
        "service": "Financial Migration Simulator",
        "version": "0.2.6"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/simulate")
def run_simulation(data: SimulationInput):
   
    try:

        # ---------- Inputs ----------
        inputs = FinancialInputs(**data.model_dump())

        # ---------- Projection ----------
        engine = ProjectionEngine(inputs)
        result = engine.simulate(force=True)

        # ---------- Financial score ----------
        scorer = FinancialScorer(inputs)
        score = scorer.calculate(result)

        # ---------- Diagnosis ----------
        diagnosis = FinancialDiagnostics.build_diagnosis(score)

        # ---------- Monte Carlo risk ----------
        monte_carlo = MonteCarloSimulator(inputs, runs=500)
        monte_result = monte_carlo.run()

        # ---------- Immigration Risk ----------
        risk_analyzer = ImmigrationRiskAnalyzer()
        risk = risk_analyzer.calculate_risk(result, score)

        # ---------- Migration Readiness ----------
        readiness_engine = MigrationReadinessIndex()
        readiness = readiness_engine.calculate(result, score, risk)


        # ---------- Response ----------
        return {
            "migration_readiness": readiness,

            "final_balance": round(result.final_balance, 2),

            "goal_reached_month": result.goal_reached_month,

            "went_negative_during_simulation": result.went_negative_during_simulation,

            "score": round(score["total_score"], 2),

            "diagnosis": diagnosis,

            "immigration_risk": risk,

            "monte_carlo": {
                "success_rate": round(monte_result.success_rate * 100, 2),
                "failure_rate": round(monte_result.failure_rate * 100, 2),
                "average_final_balance": round(monte_result.average_final_balance, 2),
                "worst_balance": round(monte_result.worst_balance, 2),
                "runs": monte_result.simulations_run,
            },

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

