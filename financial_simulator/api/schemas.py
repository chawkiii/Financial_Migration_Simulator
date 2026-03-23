# financial_simulator/api/schemas.py

from pydantic import BaseModel, model_validator
from typing import Optional, Dict


class SimulationRequest(BaseModel):
    initial_savings: float
    monthly_income: float

    monthly_expenses: Optional[float] = None
    expenses: Optional[Dict[str, float]] = None

    months: int
    savings_goal: float
    one_time_cost: float = 0
    months_without_income: int = 0

    province: str

    # ✅ VALIDATION API LEVEL
    @model_validator(mode="after")
    def validate_expenses(self):
        if self.monthly_expenses is None and self.expenses is None:
            raise ValueError("Provide either monthly_expenses or expenses")

        if self.monthly_expenses is not None and self.expenses is not None:
            raise ValueError("Provide either monthly_expenses OR expenses, not both")

        return self