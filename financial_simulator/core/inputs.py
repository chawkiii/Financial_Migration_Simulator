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
        tax_rate: float = 0.0,
        future_purchases: list[dict] | None = None,
        province: str | None = None
    ):

        self.initial_savings = initial_savings
        self.one_time_cost = one_time_cost
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.months = months
        self.savings_goal = savings_goal
        self.months_without_income = months_without_income
        self.expenses = expenses

        self.tax_rate = tax_rate
        self.future_purchases = future_purchases or []
        self.province = province

        # NEW
        self.cost_of_living_index = 1.0

        # Province adjustments
        if self.province:

            from financial_simulator.data.provinces import get_province

            province_data = get_province(self.province)

            # Apply tax rate only if user did not override
            if self.tax_rate == 0.0:
                self.tax_rate = province_data["tax_rate"]

            # Store index (do NOT modify user expenses)
            self.cost_of_living_index = province_data["cost_of_living_index"]

        self.validate()

    # =============================
    # Validation
    # =============================

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
            # Allowed but risky
            pass

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

    # =============================
    # Expenses helper
    # =============================

    def get_total_expenses(self) -> float:

        if self.expenses:
            return sum(self.expenses.values())

        return self.monthly_expenses