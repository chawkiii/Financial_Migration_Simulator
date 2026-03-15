# financial_simulator/analysis/province_optimizer.py

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.data.provinces import PROVINCES_DATA
from financial_simulator.core.inputs import FinancialInputs


class ProvinceOptimizer:

    def __init__(self):

        self.engine_class = ProjectionEngine
        self.scorer = FinancialScorer
        self.risk_analyzer = ImmigrationRiskAnalyzer()

    def rank_provinces(self, base_inputs):

        rankings = []

        for province, data in PROVINCES_DATA.items():

            adjusted_expenses = (
                base_inputs.monthly_expenses *
                data["cost_of_living_index"]
            )

            inputs = FinancialInputs(
                **base_inputs.model_dump(),
                monthly_expenses=adjusted_expenses
            )

            result = self._evaluate(inputs)

            rankings.append({
                "province": province,
                "score": result["score"],
                "risk_score": result["risk_score"],
                "risk_level": result["risk_level"],
                "final_balance": result["final_balance"]
            })

        rankings.sort(
            key=lambda x: (x["score"], -x["risk_score"]),
            reverse=True
        )

        return rankings


    def _evaluate(self, inputs):

        engine = self.engine_class(inputs)
        result = engine.simulate(force=True)

        score = self.scorer(inputs).calculate(result)

        risk = self.risk_analyzer.calculate_risk(result, score)

        return {
            "score": score["total_score"],
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
            "final_balance": result.final_balance
        }