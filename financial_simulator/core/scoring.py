# financial_simulator/core/scoring.py
from financial_simulator.core.models import ProjectionResult
from financial_simulator.core.inputs import FinancialInputs


class FinancialScorer:
    def __init__(self, inputs: FinancialInputs):
        self.inputs = inputs

    def calculate(self, result: ProjectionResult) -> dict:
        total_expenses = self.inputs.get_total_expenses()
        initial_balance = self.inputs.initial_savings - self.inputs.one_time_cost

        score = 0

        # =============================
        # 1️⃣ Survival (25)
        # =============================
        if total_expenses == 0:
            survival_points = 25
        else:
            survival_ratio = initial_balance / total_expenses

            if initial_balance <= 0 or result.insolvent_before_income:
                survival_points = 0
            elif survival_ratio >= 6:
                survival_points = 25
            elif survival_ratio >= 4:
                survival_points = 20
            elif survival_ratio >= 2:
                survival_points = 15
            elif survival_ratio >= 1:
                survival_points = 10
            else:
                survival_points = 5

        score += survival_points

        # =============================
        # 2️⃣ Margin (20)
        # =============================
        margin = self.inputs.monthly_income - total_expenses

        if margin >= 1000:
            margin_points = 20
        elif margin >= 500:
            margin_points = 15
        elif margin >= 200:
            margin_points = 10
        elif margin > 0:
            margin_points = 5
        else:
            margin_points = 0

        score += margin_points

        # =============================
        # 3️⃣ Stability (15)
        # =============================
        if result.went_negative_during_simulation:
            stability_points = 0
        elif result.max_negative_balance < 0:
            stability_points = 5
        else:
            stability_points = 15

        score += stability_points

        # =============================
        # 4️⃣ Goal (10)
        # =============================
        if result.goal_reached_month is None:
            goal_points = 0
        else:
            goal_points = 10

        score += goal_points

        # =============================
        # 5️⃣ Growth (15)
        # =============================
        growth_amount = result.final_balance - initial_balance

        if growth_amount >= self.inputs.savings_goal:
            growth_points = 15
        elif growth_amount >= self.inputs.savings_goal * 0.5:
            growth_points = 10
        elif growth_amount > 0:
            growth_points = 5
        else:
            growth_points = 0

        score += growth_points

        # =============================
        # 6️⃣ Cushion Final (15)
        # =============================
        if total_expenses == 0:
            cushion_points = 15
        else:
            cushion_months = result.final_balance / total_expenses

            if cushion_months >= 6:
                cushion_points = 15
            elif cushion_months >= 4:
                cushion_points = 10
            elif cushion_months >= 2:
                cushion_points = 5
            else:
                cushion_points = 0

        score += cushion_points

        score = max(0, min(score, 100))

        return {
            "total_score": score,
            "survival": survival_points,
            "margin": margin_points,
            "stability": stability_points,
            "growth": growth_points,
            "cushion": cushion_points,
            "goal": goal_points,
        }