# financial_simulator/core/engine.py (V2.1)
from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.models import MonthlyProjection, ProjectionResult
from math import ceil


class ProjectionEngine:
    def __init__(self, financial_inputs: FinancialInputs):
        self.inputs = financial_inputs

    # =============================
    # Core Helpers
    # =============================

    def _get_initial_balance(self) -> float:
        return self.inputs.initial_savings - self.inputs.one_time_cost

    def _get_monthly_cashflow(self, month: int) -> float:
        if month <= self.inputs.months_without_income:
            return -self.inputs.get_total_expenses()
        return self.inputs.monthly_income - self.inputs.get_total_expenses()

    def _get_minimum_required_before_income(self) -> float:
        return self.inputs.months_without_income * self.inputs.get_total_expenses()

    # =============================
    # Simulation
    # =============================

    def simulate(self, force=False) -> ProjectionResult:
        projections = []
        goal_reached_month = None
        went_negative_during_simulation = False
        insolvent_before_income = False

        current_balance = self._get_initial_balance()
        minimum_required = self._get_minimum_required_before_income()

        # Insolvabilité avant le premier revenu
        if current_balance < minimum_required:
            insolvent_before_income = True
            if not force:
                return ProjectionResult(
                    projections=[],
                    final_balance=current_balance,
                    goal_reached_month=None,
                    went_negative_during_simulation=False,
                    insolvent_before_income=True,
                    max_negative_balance=min(0, current_balance),
                    average_cashflow=0,
                    min_cushion=0,
                )

        # Boucle sur tous les mois
        for month in range(1, self.inputs.months + 1):
            starting_balance = current_balance
            monthly_cashflow = self._get_monthly_cashflow(month)
            ending_balance = starting_balance + monthly_cashflow

            if ending_balance < 0:
                went_negative_during_simulation = True

            if ending_balance >= self.inputs.savings_goal and goal_reached_month is None:
                goal_reached_month = month

            projections.append(
                MonthlyProjection(
                    month_number=month,
                    starting_balance=starting_balance,
                    net_cashflow=monthly_cashflow,
                    ending_balance=ending_balance,
                )
            )

            current_balance = ending_balance

        # Statistiques globales
        net_cashflows = [p.net_cashflow for p in projections] if projections else [0]
        balances = [p.ending_balance for p in projections] if projections else [current_balance]
        min_cushion = min(b / self.inputs.get_total_expenses() if self.inputs.get_total_expenses() > 0 else 0 for b in balances)

        return ProjectionResult(
            projections=projections,
            final_balance=current_balance,
            goal_reached_month=goal_reached_month,
            went_negative_during_simulation=went_negative_during_simulation,
            insolvent_before_income=insolvent_before_income,
            max_negative_balance=min(0, min(balances)),
            average_cashflow=sum(net_cashflows) / len(net_cashflows),
            min_cushion=min_cushion,
        )

    # =============================
    # Goal Forecast
    # =============================

    def months_to_reach_goal(self) -> int | None:
        balance = self._get_initial_balance()
        balance -= self._get_minimum_required_before_income()

        if balance >= self.inputs.savings_goal:
            return self.inputs.months_without_income

        net_cashflow = self.inputs.monthly_income - self.inputs.get_total_expenses()
        if net_cashflow <= 0:
            return None

        remaining = self.inputs.savings_goal - balance
        months_after_income = ceil(remaining / net_cashflow)
        return self.inputs.months_without_income + months_after_income

    # =============================
    # Scoring / Diagnostics
    # =============================

    def interpret_score(self, total_score: int) -> str:
        if total_score >= 80:
            return "Excellent"
        elif total_score >= 60:
            return "Stable"
        elif total_score >= 40:
            return "Fragile"
        else:
            return "High Risk"

    def generate_diagnosis(self, score: dict) -> list:
        messages = []
        if score["survival"] == 0:
            messages.append("Your emergency savings are insufficient.")
        if score["margin"] == 0:
            messages.append("Your monthly expenses exceed your income.")
        if score["growth"] == 0:
            messages.append("Your financial situation is not improving.")
        if score["cushion"] <= 5:
            messages.append("Your safety cushion is very thin.")
        if score["goal"] == 0:
            messages.append("Your savings goal is not reachable within the timeframe.")
        if not messages:
            messages.append("Your financial profile looks healthy.")
        return messages