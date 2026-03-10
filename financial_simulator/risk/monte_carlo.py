# financial_simulator/risk/monte_carlo.py

import random
from dataclasses import dataclass
from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.core.inputs import FinancialInputs


@dataclass
class MonteCarloResult:
    success_rate: float
    failure_rate: float
    worst_balance: float
    average_final_balance: float
    simulations_run: int


class MonteCarloSimulator:

    def __init__(
        self,
        inputs: FinancialInputs,
        runs: int = 500,
        income_volatility: float = 0.15,
        expense_volatility: float = 0.10,
    ):
        self.inputs = inputs
        self.runs = runs
        self.income_volatility = income_volatility
        self.expense_volatility = expense_volatility

    def _randomize_inputs(self) -> FinancialInputs:

        income_variation = random.uniform(
            -self.income_volatility,
            self.income_volatility
        )

        expense_variation = random.uniform(
            -self.expense_volatility,
            self.expense_volatility
        )

        return FinancialInputs(
            initial_savings=self.inputs.initial_savings,
            one_time_cost=self.inputs.one_time_cost,
            monthly_income=self.inputs.monthly_income * (1 + income_variation),
            monthly_expenses=self.inputs.monthly_expenses * (1 + expense_variation),
            months=self.inputs.months,
            savings_goal=self.inputs.savings_goal,
            months_without_income=self.inputs.months_without_income,
            expenses=self.inputs.expenses
        )

    def run(self) -> MonteCarloResult:

        successes = 0
        worst_balance = float("inf")
        final_balances = []

        for _ in range(self.runs):

            randomized_inputs = self._randomize_inputs()

            engine = ProjectionEngine(randomized_inputs)
            result = engine.simulate(force=True)

            final_balances.append(result.final_balance)

            worst_balance = min(worst_balance, result.final_balance)

            if result.final_balance >= randomized_inputs.savings_goal:
                successes += 1

        success_rate = successes / self.runs
        failure_rate = 1 - success_rate

        average_final = sum(final_balances) / len(final_balances)

        return MonteCarloResult(
            success_rate=success_rate,
            failure_rate=failure_rate,
            worst_balance=worst_balance,
            average_final_balance=average_final,
            simulations_run=self.runs
        )