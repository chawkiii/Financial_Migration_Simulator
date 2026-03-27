# financial_simulator/core/engine.py

from financial_simulator.core.models import ProjectionResult

class ProjectionEngine:

    # total_outflow = expenses + taxes + purchases
    # net_cashflow = income - total_outflow

    def __init__(self, inputs):
        self.inputs = inputs

    # =============================
    # MAIN ENTRY
    # =============================
    def simulate(
        self,
        monthly_income=None,
        monthly_expenses=None,
        monthly_hook=None,
        force=False
    ) -> ProjectionResult:

        state = self._initialize_state()

        for month in range(1, self.inputs.config.months + 1):

            self._process_month(
                state,
                month,
                monthly_income,
                monthly_expenses,
                monthly_hook
            )

            if not force and state["balance"] < 0:
                break

        return self._build_result(state)

    # =============================
    # INITIALIZATION
    # =============================
    def _initialize_state(self):

        initial_balance = (
            self.inputs.profile.initial_savings
            - self.inputs.config.one_time_cost
        )

        return {
            "balance": initial_balance,
            "initial_balance": initial_balance,

            "monthly_records": [],

            "total_tax_paid": 0,
            "total_gross_income": 0,
            "total_net_income": 0,
            "total_expenses": 0,

            "went_negative": False,
            "insolvent_before_income": initial_balance < 0,
            "max_negative_balance": 0,

            "goal_reached_month": None,
        }

    # =============================
    # MONTH PROCESSING
    # =============================
    def _process_month(self, state, month, monthly_income, monthly_expenses, monthly_hook):

        # ✅ fallback intelligent
        income = monthly_income if monthly_income is not None else self.inputs.profile.monthly_income

        if monthly_expenses is not None:
            expenses = monthly_expenses
        else:
            expenses = self.inputs.get_total_expenses()

        cashflow = income - expenses

        # hook
        if monthly_hook:
            cashflow = monthly_hook(month, cashflow)

        state["balance"] += cashflow

        # tracking
        state["total_net_income"] += income
        state["total_expenses"] += expenses

        if state["balance"] < 0:
            state["went_negative"] = True
            state["max_negative_balance"] = min(
                state["max_negative_balance"],
                state["balance"]
            )

        if (
            not state["goal_reached_month"]
            and state["balance"] >= self.inputs.savings_goal  # dans l'idéal tracker l'objectif chaque mois et pas juste le premier mois où on l'atteint.
        ):
            state["goal_reached_month"] = month

        state["monthly_records"].append({
            "month": month,
            "balance": state["balance"],
            "net_income": income,
            "expenses": expenses,
        })



    # =============================
    # RESULT BUILDER
    # =============================
    def _build_result(self, state) -> ProjectionResult:

        months = len(state["monthly_records"])

        avg_net_income = (
            state["total_net_income"] / months if months else 0
        )

        avg_expenses = (
            state["total_expenses"] / months if months else 0
        )

        tax_rate_effective = (
            state["total_tax_paid"] / state["total_gross_income"]
            if state["total_gross_income"] > 0 else 0
        )

        result = ProjectionResult()

        result.final_balance = state["balance"]
        result.avg_net_income = avg_net_income
        result.avg_monthly_expenses = avg_expenses
        result.total_tax_paid = state["total_tax_paid"]

        result.went_negative_during_simulation = state["went_negative"]
        result.max_negative_balance = state["max_negative_balance"]
        result.goal_reached_month = state["goal_reached_month"]
        result.insolvent_before_income = state["insolvent_before_income"]

        result.monthly_balances = [r["balance"] for r in state["monthly_records"]]

        return result