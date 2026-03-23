# financial_simulator/core/inputs/financial_profile.py

class FinancialProfile:
    def __init__(
        self,
        initial_savings: float,
        monthly_income: float,
        expenses: dict[str, float] | None = None,
        monthly_expenses: float | None = None,
    ):
        self.initial_savings = initial_savings
        self.monthly_income = monthly_income
        self.expenses = expenses if expenses is not None else None
        self.monthly_expenses = monthly_expenses

        self.validate()

    def validate(self):
        if self.initial_savings < 0:
            raise ValueError("Initial savings cannot be negative")

        if self.monthly_income < 0:
            raise ValueError("Income cannot be negative")

        if self.monthly_expenses is not None and self.monthly_expenses < 0:
            raise ValueError("Expenses cannot be negative")

        if self.expenses:
            for key, value in self.expenses.items():
                if value < 0:
                    raise ValueError(f"Expense '{key}' cannot be negative")
    
    def get_base_expenses(self):
        if self.expenses is None and self.monthly_expenses is None:
            raise ValueError("Either expenses breakdown or monthly_expenses must be provided")

        if self.expenses is not None:
            return sum(self.expenses.values())

        return self.monthly_expenses
    
    
    def get_total_expenses(self):
        if self.expenses is not None:
            return sum(self.expenses.values())

        if self.monthly_expenses is not None:
            return self.monthly_expenses

        raise ValueError("No expenses defined")