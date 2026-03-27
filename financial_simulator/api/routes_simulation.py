# financial_simulator/api/routes_simulation.py

from fastapi import APIRouter, HTTPException

from financial_simulator.core.inputs import build_inputs
from financial_simulator.core.simulation_pipeline import SimulationPipeline
from financial_simulator.analysis.scenario_explorer import MigrationScenarioExplorer
from financial_simulator.analysis.province_optimizer import ProvinceOptimizer
from financial_simulator.analysis.insights_engine import InsightsEngine
from financial_simulator.core.models.response import SimulationResponse

from .schemas import SimulationRequest

router = APIRouter()


@router.post("/simulate")
def simulate(request: SimulationRequest):

    try:
        inputs = build_inputs(request)

        pipeline = SimulationPipeline(inputs)
        result = pipeline.run()

        projection = result["projection"]

        # =========================
        # SCENARIOS
        # =========================
        explorer = MigrationScenarioExplorer()

        income_scenarios = explorer.explore_income_range(
            inputs,
            [
                inputs.profile.monthly_income * 0.8,
                inputs.profile.monthly_income,
                inputs.profile.monthly_income * 1.2,
            ]
        )

        # =========================
        # OPTIMIZATION
        # =========================
        optimizer = ProvinceOptimizer(
            inputs,
            inputs.context.all_provinces_data
        )

        province_results = optimizer.find_best_provinces()

        # =========================
        # INSIGHTS
        # =========================
        insights = InsightsEngine(
            inputs,
            projection,
            result["score"],
            province_results
        ).generate()

        # =========================
        # FINAL RESPONSE
        # =========================
        response = SimulationResponse(
            projection=projection,
            score=result["score"],
            risk=result["risk"],
            success=result["success"],
            readiness=result["readiness"],
            insights=insights,
            recommendations=result["recommendations"],
            strategy=result["strategy"],
            scenarios={
                "income_variations": income_scenarios
            },
            optimization=province_results,
            monte_carlo=result["monte_carlo"]
        )

        return response.to_dict()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))