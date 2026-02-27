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
    ):
        self.initial_savings = initial_savings
        self.one_time_cost = one_time_cost
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.months = months
        self.savings_goal = savings_goal
        self.months_without_income = months_without_income

        self.validate()

    def validate(self):
        if self.months <= 0:
            raise ValueError("Months must be greater than 0")
        
        if self.months_without_income < 0:
            raise ValueError("months_without_income cannot be negative")
        
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