# financial_simulator/tests/test_engine.py
import json
import random
import pytest

from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.analysis.diagnostics import FinancialDiagnostics
from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.risk.monte_carlo import MonteCarloSimulator


def create_default_inputs(**overrides):
    base = dict(
        initial_savings=5000,
        one_time_cost=0,
        monthly_income=3000,
        monthly_expenses=1000,
        months=12,
        savings_goal=10000,
        months_without_income=0,
    )
    base.update(overrides)
    return FinancialInputs(**base)

def test_zero_expenses():
    inputs = create_default_inputs(monthly_expenses=0)
    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.min_cushion == 0


# =========================
# Projection core
# =========================

def test_projection_result_serializable():

    inputs = create_default_inputs(months=2)

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    result_dict = result.to_dict()

    json.dumps(result_dict)

    assert isinstance(result_dict["projections"], list)


def test_negative_margin_triggers_negative_balance():

    inputs = create_default_inputs(
        initial_savings=1000,
        monthly_income=1000,
        monthly_expenses=1500,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.went_negative_during_simulation is True


def test_goal_reached():

    inputs = create_default_inputs(
        initial_savings=10000,
        monthly_income=3000,
        monthly_expenses=1000,
        savings_goal=15000,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.goal_reached_month is not None


# =========================
# Financial scoring
# =========================

def test_score_range():

    inputs = create_default_inputs()

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    scorer = FinancialScorer(inputs)
    score = scorer.calculate(result)

    assert 0 <= score["total_score"] <= 100


# =========================
# Diagnostics
# =========================

def test_interpret_score_levels():

    assert FinancialDiagnostics.interpret_score(85) == "Excellent"
    assert FinancialDiagnostics.interpret_score(65) == "Stable"
    assert FinancialDiagnostics.interpret_score(45) == "Fragile"
    assert FinancialDiagnostics.interpret_score(20) == "High Risk"


def test_build_diagnosis_structure():

    fake_score = {
        "survival": 0,
        "margin": 0,
        "stability": 0,
        "growth": 0,
        "cushion": 0,
        "goal": 0,
        "total_score": 0,
    }

    diagnosis = FinancialDiagnostics.build_diagnosis(fake_score)

    assert isinstance(diagnosis, dict)
    assert "level" in diagnosis
    assert isinstance(diagnosis["messages"], list)


# =========================
# Insolvency scenarios
# =========================

def test_insolvent_before_income():

    inputs = create_default_inputs(
        initial_savings=1000,
        monthly_expenses=1000,
        months_without_income=2,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.insolvent_before_income is True


def test_zero_income_scenario():

    inputs = create_default_inputs(
        monthly_income=0,
        monthly_expenses=1500,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.went_negative_during_simulation is True


def test_negative_cashflow_but_positive_balance():

    inputs = create_default_inputs(
        initial_savings=10000,
        monthly_income=2000,
        monthly_expenses=3000,
        months=6,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.went_negative_during_simulation is False


# =========================
# Engine metrics
# =========================

def test_max_negative_balance():

    inputs = create_default_inputs(
        initial_savings=1000,
        monthly_income=0,
        monthly_expenses=1500,
        months=2,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.max_negative_balance == -2000


def test_average_cashflow():

    inputs = create_default_inputs(
        months=2
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.average_cashflow == 2000


def test_min_cushion():

    inputs = create_default_inputs(
        initial_savings=6000,
        monthly_income=0,
        monthly_expenses=2000,
        months=2,
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.min_cushion == 1


# =========================
# Expense system
# =========================

def test_categorized_expenses_override_monthly():

    inputs = create_default_inputs(
        months=1,
        monthly_expenses=9999,
        expenses={
            "rent": 1000,
            "food": 500,
        }
    )

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    assert result.projections[0].net_cashflow == 1500


# =========================
# Risk engine
# =========================

def test_risk_score_range():

    inputs = create_default_inputs()

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    scorer = FinancialScorer(inputs)
    score = scorer.calculate(result)

    analyzer = ImmigrationRiskAnalyzer()
    risk = analyzer.calculate_risk(result, score)

    assert 0 <= risk["risk_score"] <= 100


# =========================
# Monte Carlo
# =========================

def test_monte_carlo_runs():

    inputs = create_default_inputs()

    simulator = MonteCarloSimulator(inputs, runs=50)
    result = simulator.run()

    assert 0 <= result.success_rate <= 1
    assert result.simulations_run == 50


# =========================
# Robustness / fuzz testing
# =========================

def test_randomized_simulations_do_not_crash():

    for _ in range(100):

        inputs = FinancialInputs(
            initial_savings=random.randint(0, 20000),
            one_time_cost=random.randint(0, 5000),
            monthly_income=random.randint(0, 5000),
            monthly_expenses=random.randint(500, 4000),
            months=random.randint(1, 24),
            months_without_income=random.randint(0, 6),
            savings_goal=random.randint(0, 30000),
        )

        engine = ProjectionEngine(inputs)
        result = engine.simulate(force=True)

        assert result.final_balance is not None
        assert isinstance(result.final_balance, (int, float))