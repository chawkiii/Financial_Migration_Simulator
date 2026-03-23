# financial_simulator/analysis/province_optimizer.py

from concurrent.futures import ThreadPoolExecutor

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.data.provinces import PROVINCES_DATA
from financial_simulator.core.inputs import SimulationInputs


class ProvinceOptimizer:
    """Optimizes and ranks Canadian provinces based on financial simulation outcomes."""

    def __init__(self):
        self.risk_analyzer = ImmigrationRiskAnalyzer()

    # =============================
    # 1️⃣ Rank Provinces
    # =============================
    def rank_provinces(self, base_inputs: SimulationInputs) -> list[dict]:
        tasks = []

        # Clone inputs for each province
        for province, data in PROVINCES_DATA.items():
            inputs_data = base_inputs.model_dump()
            inputs_data.update({
                "province": province,
                "tax_rate": data.get("tax_rate", 0)
            })

            inputs = SimulationInputs(**inputs_data)
            inputs.cost_of_living_index = data.get("cost_of_living_index", 1.0)

            tasks.append((province, inputs))

        # Parallel execution
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(self._evaluate_province, tasks))

        # Sort: success probability → lower risk → higher final balance
        results.sort(
            key=lambda x: (x["score"], -x["risk_score"], x["final_balance"]),
            reverse=True
        )

        return results

    # =============================
    # 2️⃣ Evaluate Province
    # =============================
    def _evaluate_province(self, task: tuple) -> dict:
        province, inputs = task
        province_data = PROVINCES_DATA[province]

        # Run financial projection
        engine = ProjectionEngine(inputs)
        result = engine.simulate(force=True)

        # Compute financial score
        scorer = FinancialScorer(inputs)
        score = scorer.calculate(result)

        # Analyze risk
        risk = self.risk_analyzer.calculate_risk(result, score)

        return {
            "province": province,
            "score": score["total_score"],
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
            "final_balance": result.final_balance,
            "job_market_score": province_data.get("job_market_score", 0),
            "avg_salary": province_data.get("avg_salary", 0),
            "tax_rate": province_data.get("tax_rate", 0),
            "cost_of_living_index": province_data.get("cost_of_living_index", 1.0)
        }