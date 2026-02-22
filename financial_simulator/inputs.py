class FinancialInputs:
    def __init__(
        self,
        initial_savings: float,
        one_time_cost: float,
        monthly_income: float,
        monthly_expenses: float,
        months: int,
        savings_goal: float,
    ):
        self.initial_savings = initial_savings
        self.one_time_cost = one_time_cost
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.months = months
        self.savings_goal = savings_goal

        self.validate()

    def validate(self):
        if self.months <= 0:
            raise ValueError("Months must be greater than 0")

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