# financial_simulator/api/routes_simulation.py

from fastapi import APIRouter, HTTPException

from financial_simulator.api.schemas import SimulationInput
from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.simulation_pipeline import SimulationPipeline

router = APIRouter()


@router.post("/simulate")
def run_simulation(data: SimulationInput):

    try:

        inputs = FinancialInputs(**data.model_dump())

        pipeline = SimulationPipeline()
        output = pipeline.run(inputs)

        result = output["projection"]
        score = output["score"]
        insights = output["insights"]
        risk = output["risk"]
        monte_carlo = output["monte_carlo"]
        success = output["success_probability"]
        strategy = output["strategy"]

        return {

            "simulation": {

                "final_balance": round(result.final_balance, 2),

                "goal_reached_month": result.goal_reached_month,

                "went_negative": result.went_negative_during_simulation,

                "insolvent_before_income": result.insolvent_before_income,

                "max_negative_balance": round(result.max_negative_balance, 2),

                "average_cashflow": round(result.average_cashflow, 2),

                "min_cushion": round(result.min_cushion, 2),

                "monthly_projections": [
                    {
                        "month": p.month_number,
                        "start": round(p.starting_balance, 2),
                        "end": round(p.ending_balance, 2),
                        "cashflow": round(p.net_cashflow, 2),
                    }
                    for p in result.projections
                ]
            },


            "analysis": {

                "financial_score": round(score["total_score"], 2),
                "interpretation": score["interpretation"],
                "insights": insights
            },

            "risk": risk,

            "monte_carlo": {

                "success_rate": round(monte_carlo.success_rate * 100, 2),
                "failure_rate": round(monte_carlo.failure_rate * 100, 2),
                "average_final_balance": round(monte_carlo.average_final_balance, 2),
                "worst_balance": round(monte_carlo.worst_balance, 2),
                "simulations_run": monte_carlo.simulations_run
            },

            "success_probability": success,

            "strategy": strategy
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))