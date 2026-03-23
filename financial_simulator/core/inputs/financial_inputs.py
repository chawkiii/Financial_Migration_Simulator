# financial_simulator/core/inputs/financial_inputs.py

from .simulation_inputs import SimulationInputs
from .financial_profile import FinancialProfile
from .simulation_config import SimulationConfig
from .economic_context import EconomicContext


class FinancialInputs(SimulationInputs):

    def __init__(
        self,
        initial_savings,
        monthly_income,
        monthly_expenses=None,
        expenses=None,
        months=12,
        savings_goal=0,
        one_time_cost=0,
        months_without_income=0,
        province="ontario",
    ):

        profile = FinancialProfile(
            initial_savings=initial_savings,
            monthly_income=monthly_income,
            monthly_expenses=monthly_expenses,
            expenses=expenses,
        )

        config = SimulationConfig(
            months=months,
            savings_goal=savings_goal,
            one_time_cost=one_time_cost,
            months_without_income=months_without_income,
        )

        context = EconomicContext(
            province=province,
        )

        super().__init__(profile, config, context)

        self.normalize()
        self.validate()