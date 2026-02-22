from inputs import FinancialInputs
from models import MonthlyProjection, ProjectionResult


class ProjectionEngine:
    def __init__(self, financial_inputs: FinancialInputs):
        self.inputs = financial_inputs

    def calculate_monthly_cashflow(self) -> float:
        return self.inputs.monthly_income - self.inputs.monthly_expenses

    def simulate(self) -> ProjectionResult:
        projections = []

        current_balance = (
            self.inputs.initial_savings - self.inputs.one_time_cost
        )

        net_cashflow = self.calculate_monthly_cashflow()

        goal_reached_month = None
        went_negative = False

        for month in range(1, self.inputs.months + 1):
            starting_balance = current_balance
            ending_balance = starting_balance + net_cashflow

            if ending_balance < 0:
                went_negative = True

            if (
                ending_balance >= self.inputs.savings_goal
                and goal_reached_month is None
            ):
                goal_reached_month = month

            projection = MonthlyProjection(
                month_number=month,
                starting_balance=starting_balance,
                net_cashflow=net_cashflow,
                ending_balance=ending_balance,
            )

            projections.append(projection)

            current_balance = ending_balance

        return ProjectionResult(
            projections=projections,
            final_balance=current_balance,
            goal_reached_month=goal_reached_month,
            went_negative=went_negative,
        )
    
    def months_to_reach_goal(self) -> int | None:
        current_balance = (
            self.inputs.initial_savings - self.inputs.one_time_cost
        )

        net_cashflow = self.calculate_monthly_cashflow()

        if net_cashflow <= 0:
            return None  # Impossible d’atteindre l’objectif

        month = 0

        while current_balance < self.inputs.savings_goal:
            current_balance += net_cashflow
            month += 1

        return month