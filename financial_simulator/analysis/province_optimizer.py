# financial_simulator/analysis/province_optimizer.py

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.core.inputs import SimulationInputs


class ProvinceOptimizer:

    def __init__(self, base_inputs: SimulationInputs, provinces_data: dict):
        self.base_inputs = base_inputs
        self.provinces_data = provinces_data

    # =============================
    # MAIN ENTRY
    # =============================
    def find_best_provinces(self):

        results = []

        for province_name, province_data in self.provinces_data.items():

            scenario = self._simulate_province(province_name, province_data)
            results.append(scenario)

        # Sort by best score
        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "best": results[0] if results else None,
            "ranking": results
        }

    # =============================
    # SINGLE PROVINCE SIMULATION
    # =============================
    def _simulate_province(self, province_name, province_data):

        # Clone inputs with new province context
        inputs = SimulationInputs(
            profile=self.base_inputs.profile.__class__(
                initial_savings=self.base_inputs.profile.initial_savings,
                monthly_income=self.base_inputs.profile.monthly_income,
                monthly_expenses=self.base_inputs.profile.monthly_expenses,
                expenses=self.base_inputs.profile.expenses,
            ),
            config=self.base_inputs.config,
            context=self._build_context(province_name, province_data)
        )

        inputs.normalize()
        inputs.validate()

        # Run simulation
        engine = ProjectionEngine(inputs)
        result = engine.simulate(force=True)

        # Score
        scorer = FinancialScorer(inputs)
        score = scorer.calculate(result)

        return {
            "province": province_name,

            # Core metrics
            "score": score["total_score"],
            "final_balance": result.final_balance,

            # Financial insights
            "net_income": result.avg_net_income,
            "expenses": result.avg_monthly_expenses,
            "tax_rate": result.tax_rate_effective,
            "total_tax_paid": result.total_tax_paid,

            # Risk indicators
            "went_negative": result.went_negative_during_simulation,
            "max_negative_balance": result.max_negative_balance,

            # Goal tracking
            "goal_reached": bool(result.goal_reached_month),
            "goal_month": result.goal_reached_month,
        }

    # =============================
    # CONTEXT BUILDER
    # =============================
    def _build_context(self, province_name, province_data):

        return self.base_inputs.context.__class__(
            province=province_name,
            province_data=province_data
        )