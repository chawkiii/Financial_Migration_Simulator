# financial_simulator/tests/test_scenarios.py
import pytest

from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.analysis.diagnostics import FinancialDiagnostics


scenarios = [

    pytest.param(
        {
            "initial_savings": 15000,
            "one_time_cost": 4000,
            "months_without_income": 1,
            "monthly_income": 2800,
            "monthly_expenses": 2000,
            "months": 12,
            "savings_goal": 10000,
        },
        id="stable_growth"
    ),

    pytest.param(
        {
            "initial_savings": 2000,
            "one_time_cost": 3000,
            "months_without_income": 3,
            "monthly_income": 1800,
            "monthly_expenses": 2200,
            "months": 12,
            "savings_goal": 8000,
        },
        id="early_insolvency"
    ),

    pytest.param(
        {
            "initial_savings": 5000,
            "one_time_cost": 3500,
            "months_without_income": 2,
            "monthly_income": 2000,
            "monthly_expenses": 2300,
            "months": 12,
            "savings_goal": 12000,
        },
        id="slow_decline"
    ),
]


@pytest.mark.parametrize("scenario", scenarios)
def test_scenarios_run_without_crash(scenario):

    inputs = FinancialInputs(**scenario)

    engine = ProjectionEngine(inputs)
    result = engine.simulate(force=True)

    scorer = FinancialScorer(inputs)
    score = scorer.calculate(result)

    diagnosis = FinancialDiagnostics.build_diagnosis(score)

    assert result.final_balance is not None
    assert isinstance(score, dict)
    assert 0 <= score["total_score"] <= 100
    assert isinstance(diagnosis["messages"], list)