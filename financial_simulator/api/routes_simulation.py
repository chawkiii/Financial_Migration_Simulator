# financial_simulator/api/routes_simulation.py

from fastapi import APIRouter, HTTPException

from financial_simulator.api.schemas import SimulationInput
from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.simulation_pipeline import SimulationPipeline
from financial_simulator.api.schemas import ScenarioComparisonRequest
from financial_simulator.analysis.province_optimizer import ProvinceOptimizer
from financial_simulator.database.session import SessionLocal
from financial_simulator.database.models import Simulation

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

        with SessionLocal() as db:
            simulations = db.query(Simulation).all()

        simulation_record = Simulation(
            province=data.province,
            inputs=data.model_dump(),
            results={
                "final_balance": result.final_balance,
                "score": score["total_score"],
                "success_probability": success["success_probability"]
            }
        )

        db.add(simulation_record)
        db.commit()
        db.close()

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
    

@router.post("/compare")
def compare_scenarios(data: ScenarioComparisonRequest):

    pipeline = SimulationPipeline()

    results = []

    for i, scenario in enumerate(data.scenarios):

        inputs = FinancialInputs(**scenario.model_dump())

        output = pipeline.run(inputs)

        results.append({
            "name": f"Scenario {i+1}",
            "final_balance": output["projection"].final_balance,
            "financial_score": output["score"]["total_score"],
            "success_probability": output["success_probability"]["success_probability"],
            "risk_level": output["risk"]["risk_level"]
        })

    return {"scenarios": results}

@router.post("/province-ranking")
def province_ranking(data: SimulationInput):

    inputs = FinancialInputs(**data.model_dump())

    optimizer = ProvinceOptimizer()

    rankings = optimizer.rank_provinces(inputs)

    return {"rankings": rankings}


@router.get("/history")
def simulation_history():

    with SessionLocal() as db:
        simulations = db.query(Simulation).all()

    simulations = db.query(Simulation).order_by(Simulation.created_at.desc()).all()

    results = []

    for s in simulations:

        results.append({
            "id": s.id,
            "province": s.province,
            "created_at": s.created_at,
            "results": s.results
        })

    db.close()

    return {"history": results}


@router.get("/dashboard")
def user_dashboard():

    with SessionLocal() as db:
        simulations = db.query(Simulation).all()

    simulations = db.query(Simulation).all()

    total_simulations = len(simulations)

    if total_simulations == 0:
        return {
            "total_simulations": 0,
            "average_score": 0,
            "best_balance": 0
        }

    scores = []
    balances = []

    for s in simulations:

        if s.results:
            scores.append(s.results.get("score", 0))
            balances.append(s.results.get("final_balance", 0))

    db.close()

    return {

        "total_simulations": total_simulations,

        "average_score": round(sum(scores) / len(scores), 2) if scores else 0,

        "best_balance": max(balances) if balances else 0
    }


@router.get("/simulation/{simulation_id}")
def get_simulation(simulation_id: int):

    with SessionLocal() as db:
        simulations = db.query(Simulation).all()

    simulation = db.query(Simulation).filter(
        Simulation.id == simulation_id
    ).first()

    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    db.close()

    return simulation



@router.get("/analytics/provinces")
def province_stats():

    with SessionLocal() as db:
        simulations = db.query(Simulation).all()


    stats = {}

    for s in simulations:

        province = s.province

        if province not in stats:
            stats[province] = {
                "count": 0,
                "avg_score": 0
            }

        stats[province]["count"] += 1

        if s.results:
            stats[province]["avg_score"] += s.results.get("score", 0)

    for p in stats:

        stats[p]["avg_score"] = round(
            stats[p]["avg_score"] / stats[p]["count"], 2
        )

    db.close()

    return stats