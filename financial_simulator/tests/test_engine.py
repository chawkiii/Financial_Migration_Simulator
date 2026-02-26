from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.core.scoring import FinancialScorer


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
    scorer = FinancialScorer(inputs)
    score = scorer.calculate(result)

    assert 0 <= score["total_score"] <= 100

def test_insolvent_before_income():
    inputs = FinancialInputs(
        initial_savings=1000,
        one_time_cost=0,
        monthly_income=2000,
        monthly_expenses=1000,
        months=6,
        savings_goal=5000,
        months_without_income=2,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.insolvent_before_income is True


def test_months_to_reach_goal_none_if_negative_margin():
    inputs = FinancialInputs(
        initial_savings=5000,
        one_time_cost=0,
        monthly_income=1000,
        monthly_expenses=2000,
        months=12,
        savings_goal=20000,
    )

    engine = ProjectionEngine(inputs)

    assert engine.months_to_reach_goal() is None


def test_monthly_cashflow_without_income():
    inputs = FinancialInputs(
        initial_savings=5000,
        one_time_cost=0,
        monthly_income=3000,
        monthly_expenses=1000,
        months=3,
        savings_goal=10000,
        months_without_income=1,
    )

    engine = ProjectionEngine(inputs)

    assert engine._get_monthly_cashflow(1) == -1000
    assert engine._get_monthly_cashflow(2) == 2000

def test_interpret_score():
    inputs = FinancialInputs(
        initial_savings=5000,
        one_time_cost=0,
        monthly_income=4000,
        monthly_expenses=2000,
        months=12,
        savings_goal=10000,
    )

    engine = ProjectionEngine(inputs)

    assert engine.interpret_score(85) == "Excellent"
    assert engine.interpret_score(65) == "Stable"
    assert engine.interpret_score(45) == "Fragile"
    assert engine.interpret_score(20) == "High Risk"
    
def test_generate_diagnosis_returns_list():
    inputs = FinancialInputs(
        initial_savings=1000,
        one_time_cost=0,
        monthly_income=1000,
        monthly_expenses=2000,
        months=6,
        savings_goal=5000,
    )

    engine = ProjectionEngine(inputs)

    fake_score = {
        "survival": 0,
        "margin": 0,
        "growth": 0,
        "cushion": 0,
        "goal": 0,
        "total_score": 0,
    }

    diagnosis = engine.generate_diagnosis(fake_score)

    assert isinstance(diagnosis, list)
    assert len(diagnosis) > 0