# financial_simulator/core/tax/expense_tax_engine.py

class ExpenseTaxEngine:

    def __init__(self, province_data: dict):
        self.config = province_data["expense_tax"]

    def calculate_sales_tax(self, expenses: dict | None) -> float:

        if not expenses:
            return 0.0

        rules = self.config["category_rules"]
        default_rate = self.config["combined_rate"]

        total_tax = 0.0

        for category, amount in expenses.items():
            if amount <= 0:
                continue

            rate = rules.get(category, default_rate)
            total_tax += amount * rate

        return total_tax