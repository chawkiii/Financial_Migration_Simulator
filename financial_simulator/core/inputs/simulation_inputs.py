# financial_simulator/core/inputs/simulation_inputs.py

from financial_simulator.core.inputs.economic_context import EconomicContext
from financial_simulator.core.inputs.financial_profile import FinancialProfile
from financial_simulator.core.inputs.simulation_config import SimulationConfig



class SimulationInputs:
    def __init__(
        self,
        profile: FinancialProfile,
        config: SimulationConfig,
        context: EconomicContext
    ):
        self.profile = profile
        self.config = config
        self.context = context
    
    # =========================
    # HELPERS (PROXY METHODS)
    # =========================

    def get_total_expenses(self):
        return self.profile.get_total_expenses()

    def get_base_expenses(self):
        return self.profile.get_base_expenses()


    def to_dict(self):
        return {
            "profile": {
                "initial_savings": self.profile.initial_savings,
                "monthly_income": self.profile.monthly_income,
                "expenses": self.profile.expenses,
                "monthly_expenses": self.profile.monthly_expenses,
            },
            "config": {
                "months": self.config.months,
                "savings_goal": self.config.savings_goal,
                "one_time_cost": self.config.one_time_cost,
                "months_without_income": self.config.months_without_income,
            },
            "context": {
                "province": self.context.province,
            },
        }

    # =========================
    # VALIDATION (STRICT)
    # =========================
    def validate(self):

        # config coherence
        if self.config.months_without_income > self.config.months:
            raise ValueError("months_without_income cannot exceed total months")

        # expenses logic (aligned with API)
        if self.profile.expenses is None and self.profile.monthly_expenses is None:
            raise ValueError("You must provide either expenses or monthly_expenses")

        if self.profile.expenses is not None and self.profile.monthly_expenses is not None:
            raise ValueError("Provide either expenses OR monthly_expenses, not both")


    # =========================
    # NORMALIZATION (SAFE)
    # =========================
    def normalize(self):

        # floats safety
        self.profile.initial_savings = float(self.profile.initial_savings)
        self.profile.monthly_income = float(self.profile.monthly_income)

        if self.profile.monthly_expenses is not None:
            self.profile.monthly_expenses = float(self.profile.monthly_expenses)

    # ⚠️ IMPORTANT:
    # NO BUSINESS LOGIC HERE
    # taxes & real expenses handled in projection.py