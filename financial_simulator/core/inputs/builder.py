# financial_simulator/core/inputs/builder.py

from .financial_profile import FinancialProfile
from .simulation_config import SimulationConfig
from .economic_context import EconomicContext
from .simulation_inputs import SimulationInputs

from financial_simulator.data.provinces import PROVINCES_DATA


def build_inputs(data):

    # support both dict and object
    def get_attr(name, default=None):
        if isinstance(data, dict):
            return data.get(name, default)
        return getattr(data, name, default)
    # =========================
    # PROFILE
    # =========================
    profile = FinancialProfile(
        initial_savings=get_attr("initial_savings"),
        monthly_income=get_attr("monthly_income"),
        expenses=get_attr("expenses", None),
        monthly_expenses=get_attr("monthly_expenses", None),
    )

    # =========================
    # CONFIG
    # =========================
    config = SimulationConfig(
        months=data.months,
        savings_goal=data.savings_goal,
        one_time_cost=data.one_time_cost,
        months_without_income=data.months_without_income,
    )

    # =========================
    # CONTEXT
    # =========================
    province_key = data.province.lower()

    if province_key not in PROVINCES_DATA:
        raise ValueError(f"Invalid province: {data.province}")

    context = EconomicContext(
        province=province_key,
    )

    # =========================
    # FINAL INPUTS
    # =========================
    inputs = SimulationInputs(profile, config, context)

    inputs.normalize()
    inputs.validate()

    return inputs