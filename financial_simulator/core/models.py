# financial_simulator/core/models.py
from dataclasses import dataclass, field
from typing import List, Optional


# =========================
# MONTHLY PROJECTION
# =========================

@dataclass
class MonthlyProjection:
    month_number: int
    starting_balance: float
    net_cashflow: float
    ending_balance: float
    purchase_cost: float = 0.0


# =========================
# PROJECTION RESULT
# =========================

@dataclass
class ProjectionResult:
    projections: List[MonthlyProjection]
    final_balance: float
    goal_reached_month: Optional[int]
    went_negative_during_simulation: bool
    insolvent_before_income: bool

    # Metrics
    max_negative_balance: float = 0.0
    average_cashflow: float = 0.0
    min_cushion: float = 0.0

    # Future extension (taxes, analytics…)
    total_taxes_paid: float = 0.0

    def to_dict(self):
        return {
            "final_balance": self.final_balance,
            "goal_reached_month": self.goal_reached_month,
            "went_negative_during_simulation": self.went_negative_during_simulation,
            "insolvent_before_income": self.insolvent_before_income,
            "max_negative_balance": self.max_negative_balance,
            "average_cashflow": self.average_cashflow,
            "min_cushion": self.min_cushion,
            "total_taxes_paid": self.total_taxes_paid,
            "projections": [p.__dict__ for p in self.projections],
        }