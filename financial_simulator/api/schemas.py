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

    province: Optional[str] = None
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
    insolvent_before_income: bool
    max_negative_balance: float
    average_cashflow: float
    min_cushion: float
    monthly_projections: List[MonthlyProjection]


class AnalysisResult(BaseModel):
    financial_score: float
    interpretation: str
    insights: list


class SimulationResponse(BaseModel):
    simulation: SimulationResult
    analysis: AnalysisResult
    risk: dict
    monte_carlo: dict
    success_probability: dict
    strategy: list


class ScenarioComparisonRequest(BaseModel):
    scenarios: List[SimulationInput]


class ScenarioComparisonResult(BaseModel):
    name: str
    final_balance: float
    financial_score: float
    success_probability: float
    risk_level: str