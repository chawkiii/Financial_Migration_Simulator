# financial_simulator/analysis/scoring.py

from financial_simulator.core.models import ProjectionResult
from financial_simulator.core.inputs.simulation_inputs import SimulationInputs


class FinancialScorer:

    def __init__(self, inputs: SimulationInputs):
        self.inputs = inputs

    # =============================
    # MAIN ENTRY
    # =============================
    def calculate(self, result: ProjectionResult) -> dict:

        initial_balance = (
            self.inputs.profile.initial_savings
            - self.inputs.config.one_time_cost
        )

        avg_expenses = result.avg_monthly_expenses
        avg_net_income = result.avg_net_income

        score = 0

        survival = self._score_survival(initial_balance, avg_expenses, result)
        margin = self._score_margin(avg_net_income, avg_expenses)
        stability = self._score_stability(result)
        goal = self._score_goal(result)
        growth = self._score_growth(result, initial_balance)
        cushion = self._score_cushion(result, avg_expenses)
        tax_efficiency = self._score_tax_efficiency(result)

        score = (
            survival
            + margin
            + stability
            + goal
            + growth
            + cushion
            + tax_efficiency
        )

        score = max(0, min(score, 100))

        return {
            "total_score": score,
            "interpretation": self._interpret_score(score),

            "survival": survival,
            "margin": margin,
            "stability": stability,
            "growth": growth,
            "cushion": cushion,
            "goal": goal,
            "tax_efficiency": tax_efficiency,
        }

    # =============================
    # SCORING COMPONENTS
    # =============================

    def _score_survival(self, initial_balance, avg_expenses, result):

        if avg_expenses == 0:
            return 25

        if initial_balance <= 0 or result.insolvent_before_income:
            return 0

        ratio = initial_balance / avg_expenses

        if ratio >= 6:
            return 25
        elif ratio >= 4:
            return 20
        elif ratio >= 2:
            return 15
        elif ratio >= 1:
            return 10
        else:
            return 5

    def _score_margin(self, avg_net_income, avg_expenses):

        margin = avg_net_income - avg_expenses

        if margin >= 1000:
            return 20
        elif margin >= 500:
            return 15
        elif margin >= 200:
            return 10
        elif margin > 0:
            return 5
        else:
            return 0

    def _score_stability(self, result: ProjectionResult):

        if result.went_negative_during_simulation:
            return 0

        if result.max_negative_balance < 0:
            return 5

        return 15

    def _score_goal(self, result: ProjectionResult):
        return 10 if result.goal_reached_month else 0

    def _score_growth(self, result: ProjectionResult, initial_balance):

        growth = result.final_balance - initial_balance
        goal = self.inputs.config.savings_goal

        if growth >= goal:
            return 15
        elif growth >= goal * 0.5:
            return 10
        elif growth > 0:
            return 5
        else:
            return 0

    def _score_cushion(self, result: ProjectionResult, avg_expenses):

        if avg_expenses == 0:
            return 15

        cushion = result.final_balance / avg_expenses

        if cushion >= 6:
            return 15
        elif cushion >= 4:
            return 10
        elif cushion >= 2:
            return 5
        else:
            return 0

    def _score_tax_efficiency(self, result: ProjectionResult):
        """
        New component 🔥
        Rewards lower effective tax pressure.
        """

        tax_rate = result.tax_rate_effective

        if tax_rate <= 0.15:
            return 10
        elif tax_rate <= 0.25:
            return 7
        elif tax_rate <= 0.35:
            return 4
        else:
            return 0

    # =============================
    # INTERPRETATION
    # =============================

    def _interpret_score(self, score):

        if score >= 85:
            return "Excellent financial profile"
        elif score >= 70:
            return "Strong financial stability"
        elif score >= 55:
            return "Moderate risk profile"
        elif score >= 40:
            return "High risk profile"
        return "Critical financial situation"