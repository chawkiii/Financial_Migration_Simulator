# financial_simulator/core/engine.py

from financial_simulator.core.models import MonthlyProjection, ProjectionResult
from typing import Callable, Optional, List, Dict


class ProjectionEngine:

    def __init__(
        self,
        initial_savings: float,
        monthly_income: float,
        monthly_expenses: float,
        months: int,
        savings_goal: float,
        one_time_cost: float = 0,
        months_without_income: int = 0,
        future_purchases: Optional[List[Dict]] = None,
    ):
        self.initial_savings = initial_savings
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.months = months
        self.savings_goal = savings_goal
        self.one_time_cost = one_time_cost
        self.months_without_income = months_without_income
        self.future_purchases = future_purchases or []

        # achats regroupés par mois
        self.purchases_by_month = {}
        for p in self.future_purchases:
            month = p["month"]
            amount = p["amount"]
            if month <= 0:
                raise ValueError("Purchase month must be >= 1")
            self.purchases_by_month.setdefault(month, 0)
            self.purchases_by_month[month] += amount

    # -------------------------
    # LOGIQUE INTERNE
    # -------------------------

    def _initial_balance(self) -> float:
        return self.initial_savings - self.one_time_cost

    def _monthly_cashflow(self, month: int) -> float:
        if month <= self.months_without_income:
            return -self.monthly_expenses
        return self.monthly_income - self.monthly_expenses

    def _minimum_required_before_income(self) -> float:
        return self.months_without_income * self.monthly_expenses

    # -------------------------
    # SIMULATION
    # -------------------------
    def simulate(
        self,
        monthly_hook: Optional[Callable[[int, float], float]] = None,
        force: bool = False
    ) -> ProjectionResult:

        projections = []
        goal_reached_month = None
        went_negative = False
        insolvent_before_income = False

        balance = self._initial_balance()
        min_required = self._minimum_required_before_income()

        # Early failure
        if balance < min_required and not force:
            return ProjectionResult(
                projections=[],
                final_balance=balance,
                goal_reached_month=None,
                went_negative_during_simulation=False,
                insolvent_before_income=True,
                max_negative_balance=min(0, balance),
                average_cashflow=0,
                min_cushion=0,
            )

        # Boucle principale
        for month in range(1, self.months + 1):
            start_balance = balance
            cashflow = self._monthly_cashflow(month)

            # Hook pour modifier le cashflow / solde (ex: TaxEngine)
            if monthly_hook:
                cashflow = monthly_hook(month, cashflow)

            purchase_cost = self.purchases_by_month.get(month, 0)
            end_balance = start_balance + cashflow - purchase_cost

            if end_balance < 0:
                went_negative = True

            if end_balance >= self.savings_goal and goal_reached_month is None:
                goal_reached_month = month

            projections.append(
                MonthlyProjection(
                    month_number=month,
                    starting_balance=start_balance,
                    net_cashflow=cashflow,
                    ending_balance=end_balance,
                    purchase_cost=purchase_cost,
                )
            )

            balance = end_balance

        # -------------------------
        # METRICS
        # -------------------------
        net_cashflows = [p.net_cashflow for p in projections]
        balances = [p.ending_balance for p in projections]

        avg_cashflow = sum(net_cashflows) / len(net_cashflows) if net_cashflows else 0
        min_cushion = min([b / self.monthly_expenses for b in balances]) if self.monthly_expenses > 0 else 0

        return ProjectionResult(
            projections=projections,
            final_balance=balance,
            goal_reached_month=goal_reached_month,
            went_negative_during_simulation=went_negative,
            insolvent_before_income=insolvent_before_income,
            max_negative_balance=min(0, min(balances)),
            average_cashflow=avg_cashflow,
            min_cushion=min_cushion,
        )