# financial_simulator/tests/test_strategy.py

from financial_simulator.strategy.migration_strategy import MigrationStrategyPlanner


def test_strategy_returns_list():

    planner = MigrationStrategyPlanner()

    class FakeInputs:
        initial_savings = 1000
        monthly_expenses = 2000
        monthly_income = 1500
        savings_goal = 5000

    class FakeResult:
        insolvent_before_income = True
        goal_reached_month = None

    strategy = planner.suggest(FakeInputs(), FakeResult())

    assert isinstance(strategy, list)
    assert len(strategy) > 0