# financial_simulator/core/inputs.py
class FinancialInputs:
    def __init__(
        self,
        initial_savings: float,
        one_time_cost: float,
        monthly_income: float,
        monthly_expenses: float,
        months: int,
        savings_goal: float,
        months_without_income: int = 0,
        expenses: dict[str, float] | None = None,
    ):
        self.initial_savings = initial_savings
        self.one_time_cost = one_time_cost
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.months = months
        self.savings_goal = savings_goal
        self.months_without_income = months_without_income
        self.expenses = expenses

        self.validate()

    def validate(self):
        if self.months <= 0:
            raise ValueError("Projection months must be greater than zero")

        if self.monthly_income < 0:
            raise ValueError("Monthly income cannot be negative")

        if self.monthly_expenses < 0:
            raise ValueError("Monthly expenses cannot be negative")
        
        if self.months_without_income < 0:
            raise ValueError("Months without income cannot be negative")
        
        if self.one_time_cost > self.initial_savings:
            pass  # allowed but warning in result that insolvency is likely and user should consider reducing one-time cost or increasing initial savings
        
        values = [
            self.initial_savings,
            self.one_time_cost,
            self.monthly_income,
            self.monthly_expenses,
            self.savings_goal,
        ]

        for value in values:
            if value < 0:
                raise ValueError("Financial values cannot be negative")
        
    def get_total_expenses(self) -> float:
        if self.expenses:
            return sum(self.expenses.values())
        return self.monthly_expenses