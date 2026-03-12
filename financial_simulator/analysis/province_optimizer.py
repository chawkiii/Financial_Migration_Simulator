# financial_simulator/analysis/province_optimizer.py

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.data.provinces import PROVINCES_DATA
from financial_simulator.core.inputs import FinancialInputs


class ProvinceOptimizer:

    def rank_provinces(self, base_inputs):

        rankings = []

        for province, data in PROVINCES_DATA.items():

            adjusted_expenses = (
                base_inputs.monthly_expenses *
                data["cost_of_living_index"]
            )

            inputs = FinancialInputs(
                initial_savings=base_inputs.initial_savings,
                one_time_cost=base_inputs.one_time_cost,
                monthly_income=base_inputs.monthly_income,
                monthly_expenses=adjusted_expenses,
                months=base_inputs.months,
                savings_goal=base_inputs.savings_goal,
                months_without_income=base_inputs.months_without_income,
            )

            engine = ProjectionEngine(inputs)
            result = engine.simulate(force=True)

            scorer = FinancialScorer(inputs)
            score = scorer.calculate(result)

            risk_analyzer = ImmigrationRiskAnalyzer()
            risk = risk_analyzer.calculate_risk(result, score)

            rankings.append({
                "province": province,
                "score": score["total_score"],
                "risk_score": risk["risk_score"],
                "risk_level": risk["risk_level"],
                "final_balance": result.final_balance
            })

        rankings.sort(
            key=lambda x: (x["score"], -x["risk_score"]),
            reverse=True
        )

        return rankings