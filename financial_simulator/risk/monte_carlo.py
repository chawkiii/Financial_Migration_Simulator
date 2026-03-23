# financial_simulator/risk/monte_carlo.py

import random
from dataclasses import dataclass
from copy import deepcopy

from financial_simulator.core.projection import run_projection
from financial_simulator.core.inputs.simulation_inputs import SimulationInputs


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
        inputs: SimulationInputs,
        runs: int = 200,
        income_volatility: float = 0.15,
        expense_volatility: float = 0.10,
    ):
        self.inputs = inputs
        self.runs = runs
        self.income_volatility = income_volatility
        self.expense_volatility = expense_volatility

    def _randomize_inputs(self) -> SimulationInputs:

        new_inputs = deepcopy(self.inputs)

        income_variation = random.uniform(
            -self.income_volatility,
            self.income_volatility
        )

        expense_variation = random.uniform(
            -self.expense_volatility,
            self.expense_volatility
        )

        # ✅ cohérent avec ton architecture
        new_inputs.monthly_income *= (1 + income_variation)

        if new_inputs.monthly_expenses:
            new_inputs.monthly_expenses *= (1 + expense_variation)

        if new_inputs.expenses:
            for k in new_inputs.expenses:
                new_inputs.expenses[k] *= (1 + expense_variation)

        return new_inputs

    def run(self) -> MonteCarloResult:

        successes = 0
        worst_balance = float("inf")
        final_balances = []

        for _ in range(self.runs):

            randomized_inputs = self._randomize_inputs()

            result, _ = run_projection(randomized_inputs)

            final_balance = result.final_balance
            final_balances.append(final_balance)

            worst_balance = min(worst_balance, final_balance)

            if final_balance >= randomized_inputs.savings_goal:
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