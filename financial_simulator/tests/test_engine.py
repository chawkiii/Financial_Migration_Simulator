from inputs import FinancialInputs
from engine import ProjectionEngine


def test_negative_margin_triggers_negative_balance():
    inputs = FinancialInputs(
        initial_savings=1000,
        one_time_cost=0,
        monthly_income=1000,
        monthly_expenses=1500,
        months=6,
        savings_goal=5000,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.went_negative_during_simulation is True


def test_goal_reached():
    inputs = FinancialInputs(
        initial_savings=10000,
        one_time_cost=0,
        monthly_income=3000,
        monthly_expenses=1000,
        months=12,
        savings_goal=15000,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.goal_reached_month is not None


def test_score_range():
    inputs = FinancialInputs(
        initial_savings=5000,
        one_time_cost=0,
        monthly_income=4000,
        monthly_expenses=2000,
        months=12,
        savings_goal=10000,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()
    score = engine.calculate_score(result)

    assert 0 <= score["total_score"] <= 100