# financial_simulator/analysis/scoring.py

from financial_simulator.core.models import ProjectionResult
from financial_simulator.core.inputs.simulation_inputs import SimulationInputs


class FinancialScorer:

    def __init__(self, inputs: SimulationInputs, tax_summary: dict | None = None):
        self.inputs = inputs
        self.tax_summary = tax_summary or {}

    # =============================
    # MAIN ENTRY
    # =============================
    def calculate(self, result: ProjectionResult) -> dict:

        total_expenses = self.inputs.profile.get_total_expenses()
        initial_balance = self.inputs.profile.initial_savings - self.inputs.config.one_time_cost

        score = 0

        survival = self._score_survival(initial_balance, total_expenses, result)
        margin = self._score_margin(total_expenses)
        stability = self._score_stability(result)
        goal = self._score_goal(result)
        growth = self._score_growth(result, initial_balance)
        cushion = self._score_cushion(result, total_expenses)

        score = survival + margin + stability + goal + growth + cushion
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
        }

    # =============================
    # SCORING COMPONENTS
    # =============================

    def _score_survival(self, initial_balance, total_expenses, result):

        if total_expenses == 0:
            return 25

        if initial_balance <= 0 or result.insolvent_before_income:
            return 0

        ratio = initial_balance / total_expenses

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

    def _score_margin(self, total_expenses):

        net_income = self._get_monthly_net_income()

        margin = net_income - total_expenses

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

    def _score_cushion(self, result: ProjectionResult, total_expenses):

        if total_expenses == 0:
            return 15

        cushion = result.final_balance / total_expenses

        if cushion >= 6:
            return 15
        elif cushion >= 4:
            return 10
        elif cushion >= 2:
            return 5
        else:
            return 0

    # =============================
    # HELPERS
    # =============================

    def _get_monthly_net_income(self):

        if self.tax_summary and "net_income" in self.tax_summary:
            return self.tax_summary["net_income"] / 12

        return self.inputs.profile.monthly_income

    def _interpret_score(self, score):

        if score >= 80:
            return "Excellent financial stability"
        elif score >= 65:
            return "Good stability"
        elif score >= 50:
            return "Moderate risk"
        elif score >= 35:
            return "High risk"
        return "Critical financial risk"