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