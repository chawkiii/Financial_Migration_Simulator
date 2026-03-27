# financial_simulator/core/models.py
from typing import List


# =========================================
# 📅 MONTHLY PROJECTION
# =========================================
class MonthlyProjection:
    """
    Represents the financial state for a single month.
    Includes full tax breakdown and real cashflow.
    """

    def __init__(
        self,
        month: int,
        balance: float,
        income: float,
        expenses: float,
        net_income: float,
        gross_income: float,
        expense_tax: float,
        income_tax: float,
        payroll_tax: float,
    ):
        self.month = month
        self.balance = balance

        # Real values used in simulation
        self.income = income  # net income after taxes
        self.expenses = expenses  # total expenses (incl. tax)

        # Detailed breakdown (important for UI & analysis)
        self.net_income = net_income
        self.gross_income = gross_income

        self.expense_tax = expense_tax
        self.income_tax = income_tax
        self.payroll_tax = payroll_tax

    @property
    def total_tax(self) -> float:
        return self.income_tax + self.payroll_tax + self.expense_tax

    def to_dict(self) -> dict:
        return {
            "month": self.month,
            "balance": self.balance,
            "income": self.income,
            "expenses": self.expenses,
            "net_income": self.net_income,
            "gross_income": self.gross_income,
            "expense_tax": self.expense_tax,
            "income_tax": self.income_tax,
            "payroll_tax": self.payroll_tax,
            "total_tax": self.total_tax,
        }


# =========================================
# 📊 PROJECTION RESULT
# =========================================
class ProjectionResult:
    """
    Aggregated result of the full simulation.
    This is the central object used across:
    - scoring
    - risk
    - insights
    - API / frontend
    """

    def __init__(self):

        # =========================
        # CORE RESULTS
        # =========================
        self.final_balance: float = 0
        self.monthly_balances: List[float] = []
        self.monthly_projections: List[MonthlyProjection] = []

        # =========================
        # GOAL & EVENTS
        # =========================
        self.goal_reached_month: int | None = None

        # =========================
        # RISK FLAGS
        # =========================
        self.went_negative_during_simulation: bool = False
        self.insolvent_before_income: bool = False
        self.max_negative_balance: float = 0

        # =========================
        # TAX TRACKING (NEW 🔥)
        # =========================
        self.total_income_tax: float = 0
        self.total_expense_tax: float = 0
        self.total_tax_paid: float = 0

        self.monthly_tax_series: List[float] = []

        # =========================
        # AGGREGATED METRICS
        # =========================
        self.avg_net_income: float = 0
        self.avg_monthly_expenses: float = 0

    # =========================================
    # 📊 DERIVED METRICS
    # =========================================
    @property
    def min_balance(self) -> float:
        return min(self.monthly_balances) if self.monthly_balances else 0

    @property
    def min_cushion(self) -> float:
        """
        Cushion in months (how many months expenses can be covered).
        """
        if self.avg_monthly_expenses == 0:
            return 0
        return self.final_balance / self.avg_monthly_expenses

    @property
    def tax_rate_effective(self) -> float:
        """
        Effective tax pressure over the simulation.
        """
        total_gross_income = sum(m.gross_income for m in self.monthly_projections)

        if total_gross_income == 0:
            return 0

        return self.total_tax_paid / total_gross_income

    # =========================================
    # 📦 EXPORT (API READY)
    # =========================================
    def to_dict(self) -> dict:
        return {
            "final_balance": self.final_balance,
            "goal_reached_month": self.goal_reached_month,

            "went_negative": self.went_negative_during_simulation,
            "insolvent_before_income": self.insolvent_before_income,
            "max_negative_balance": self.max_negative_balance,

            "total_tax_paid": self.total_tax_paid,
            "total_income_tax": self.total_income_tax,
            "total_expense_tax": self.total_expense_tax,
            "tax_rate_effective": self.tax_rate_effective,

            "avg_net_income": self.avg_net_income,
            "avg_monthly_expenses": self.avg_monthly_expenses,
            "min_cushion": self.min_cushion,

            "monthly_balances": self.monthly_balances,
            "monthly_tax_series": self.monthly_tax_series,

            "monthly_projections": [
                m.to_dict() for m in self.monthly_projections
            ],
        }