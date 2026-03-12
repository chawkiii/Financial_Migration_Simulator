# financial_simulator/api/schemas.py

from pydantic import BaseModel
from typing import Dict, Optional, List


class SimulationInput(BaseModel):
    initial_savings: float
    one_time_cost: float
    monthly_income: float
    monthly_expenses: float
    months: int
    savings_goal: float
    months_without_income: int = 0
    expenses: Optional[Dict[str, float]] = None


class MonthlyProjection(BaseModel):
    month: int
    start: float
    end: float
    cashflow: float


class SimulationResult(BaseModel):
    final_balance: float
    goal_reached_month: int | None
    went_negative: bool
    monthly_projections: List[MonthlyProjection]


class AnalysisResult(BaseModel):
    financial_score: float
    interpretation: str
    insights: list


class SimulationResponse(BaseModel):
    simulation: SimulationResult
    analysis: AnalysisResult
    risk: dict
