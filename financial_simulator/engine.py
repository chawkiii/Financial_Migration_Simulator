from inputs import FinancialInputs
from models import MonthlyProjection, ProjectionResult
from math import ceil


class ProjectionEngine:
    def __init__(self, financial_inputs: FinancialInputs):
        self.inputs = financial_inputs

    def calculate_monthly_cashflow(self) -> float:
        return self.inputs.monthly_income - self.inputs.monthly_expenses

    def simulate(self, force=False) -> ProjectionResult:
        projections = []

        goal_reached_month = None
        went_negative_during_simulation = False
        insolvent_before_income = False

        current_balance = (
            self.inputs.initial_savings - self.inputs.one_time_cost
        )

        minimum_required = (
            self.inputs.months_without_income * self.inputs.monthly_expenses
        )

        if current_balance < minimum_required:
            insolvent_before_income = True

            if not force:
                return ProjectionResult(
                    projections=[],
                    final_balance=current_balance,
                    goal_reached_month=None,
                    went_negative_during_simulation=False,
                    insolvent_before_income=True,
                )     

        
        for month in range(1, self.inputs.months + 1):
            starting_balance = current_balance

            # Cashflow variable selon le mois
            if month <= self.inputs.months_without_income:
                monthly_cashflow = -self.inputs.monthly_expenses
            else:
                monthly_cashflow = (
                    self.inputs.monthly_income - self.inputs.monthly_expenses
                )

            ending_balance = starting_balance + monthly_cashflow

            if ending_balance < 0:
                went_negative_during_simulation = True

            if (
                ending_balance >= self.inputs.savings_goal
                and goal_reached_month is None
            ):
                goal_reached_month = month

            projection = MonthlyProjection(
                month_number=month,
                starting_balance=starting_balance,
                net_cashflow=monthly_cashflow,
                ending_balance=ending_balance,
            )

            projections.append(projection)
            current_balance = ending_balance

        return ProjectionResult(
            projections=projections,
            final_balance=current_balance,
            goal_reached_month=goal_reached_month,
            went_negative_during_simulation=went_negative_during_simulation,
            insolvent_before_income=insolvent_before_income,
        )
        
    

    def months_to_reach_goal(self) -> int | None:
        balance = self.inputs.initial_savings - self.inputs.one_time_cost

        # Appliquer les mois sans revenu
        balance -= self.inputs.months_without_income * self.inputs.monthly_expenses

        if balance >= self.inputs.savings_goal:
            return self.inputs.months_without_income

        net_cashflow = self.inputs.monthly_income - self.inputs.monthly_expenses

        if net_cashflow <= 0:
            return None

        remaining = self.inputs.savings_goal - balance
        months_after_income = ceil(remaining / net_cashflow)

        return self.inputs.months_without_income + months_after_income

    def calculate_score(self, result: ProjectionResult) -> dict:
        score = 0

        initial_balance = self.inputs.initial_savings - self.inputs.one_time_cost

        # =========================
        # 1️⃣ Survival Coverage (25)
        # =========================
        if self.inputs.monthly_expenses == 0:
            survival_points = 25
        else:
            survival_ratio = initial_balance / self.inputs.monthly_expenses

            if initial_balance <= 0:
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

        negative_months = sum(
            1 for p in result.projections if p.ending_balance < 0
        )

        survival_points -= min(negative_months * 2, 25)
        survival_points = max(survival_points, 0)

        if result.insolvent_before_income:
            survival_points = 0

        score += survival_points

        # =========================
        # 2️⃣ Monthly Margin (20)
        # =========================
        margin = self.inputs.monthly_income - self.inputs.monthly_expenses

        if margin >= 1000:
            margin_points = 20
        elif margin >= 500:
            margin_points = 15
        elif margin >= 200:
            margin_points = 10
        elif margin >= 0:
            margin_points = 5
        else:
            margin_points = 0

        score += margin_points

        # =========================
        # 3️⃣ Growth (20)
        # =========================
        if initial_balance <= 0:
            growth_points = 0
        else:
            growth_ratio = result.final_balance / initial_balance

            if growth_ratio >= 3:
                growth_points = 20
            elif growth_ratio >= 2:
                growth_points = 15
            elif growth_ratio >= 1:
                growth_points = 10
            elif growth_ratio >= 0.5:
                growth_points = 5
            else:
                growth_points = 0

        score += growth_points

        # =========================
        # 4️⃣ Cushion Reconstruction (20)
        # =========================
        target_reserve = 3 * self.inputs.monthly_expenses
        months_to_reserve = None

        for p in result.projections:
            if p.ending_balance >= target_reserve:
                months_to_reserve = p.month_number
                break

        if months_to_reserve is None:
            cushion_points = 0
        elif months_to_reserve <= 3:
            cushion_points = 20
        elif months_to_reserve <= 6:
            cushion_points = 15
        elif months_to_reserve <= 9:
            cushion_points = 10
        elif months_to_reserve <= 12:
            cushion_points = 5
        else:
            cushion_points = 0

        score += cushion_points

        # =========================
        # 5️⃣ Goal Achievement (15)
        # =========================
        if result.goal_reached_month is None:
            goal_points = 0
        elif result.goal_reached_month < self.inputs.months:
            goal_points = 15
        else:
            goal_points = 10

        score += goal_points

        score = max(0, min(score, 100))

        return {
            "total_score": score,
            "survival": survival_points,
            "margin": margin_points,
            "growth": growth_points,
            "cushion": cushion_points,
            "goal": goal_points,
        }
    
    def interpret_score(self, total_score: int) -> str:
        if total_score >= 80:
            return "Excellent"
        elif total_score >= 60:
            return "Stable"
        elif total_score >= 40:
            return "Fragile"
        else:
            return "High Risk"

    def generate_diagnosis(self, score_breakdown: dict) -> list:
        messages = []

        if score_breakdown["survival"] < 10:
            messages.append("⚠️ Insufficient emergency reserve.")

        if score_breakdown["margin"] < 10:
            messages.append("⚠️ Weak monthly margin. Consider reducing expenses or increasing income.")

        if score_breakdown["growth"] < 10:
            messages.append("⚠️ Limited growth potential.")

        if score_breakdown["cushion"] == 0:
            messages.append("⚠️ Emergency cushion not rebuilt.")

        if score_breakdown["goal"] == 0:
            messages.append("⚠️ Savings goal not achieved in projection period.")

        if not messages:
            messages.append("✅ Strong financial trajectory.")

        return messages
        