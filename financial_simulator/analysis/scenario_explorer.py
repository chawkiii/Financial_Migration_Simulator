# financial_simulator/analysis/scenario_explorer.py

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.analysis.scoring import FinancialScorer


class MigrationScenarioExplorer:

    def explore_income_range(self, base_inputs, income_values):

        scenarios = []

        for income in income_values:

            data = base_inputs.__dict__.copy()
            data["monthly_income"] = income

            inputs = FinancialInputs(**data)

            engine = ProjectionEngine(inputs)
            result = engine.simulate(force=True)

            scorer = FinancialScorer(inputs)
            score = scorer.calculate(result)

            scenarios.append({
                "income": income,
                "final_balance": result.final_balance,
                "score": score["total_score"],
                "went_negative": result.went_negative_during_simulation
            })

        return scenarios