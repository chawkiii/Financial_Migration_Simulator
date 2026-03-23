# financial_simulator/core/inputs/simulation_config.py

class SimulationConfig:
    def __init__(
        self,
        months: int,
        savings_goal: float,
        one_time_cost: float = 0,
        months_without_income: int = 0,
    ):
        self.months = months
        self.savings_goal = savings_goal
        self.one_time_cost = one_time_cost
        self.months_without_income = months_without_income

        self.validate()

    def validate(self):
        if self.months <= 0:
            raise ValueError("Months must be > 0")

        if self.months_without_income < 0:
            raise ValueError("Invalid months_without_income")
        
        if self.savings_goal < 0:
            raise ValueError("Savings goal cannot be negative")

        if self.one_time_cost < 0:
            raise ValueError("One-time cost cannot be negative")