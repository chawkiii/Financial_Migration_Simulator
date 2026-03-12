# financial_simulator/cli/main_interactive.py

from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.simulation_pipeline import SimulationPipeline
from financial_simulator.core.hints import FIELD_HINTS


def print_hint(field):
    hint = FIELD_HINTS.get(field)
    if hint:
        print(f"💡 {hint}")


def ask_float(label, field):
    print_hint(field)
    return float(input(label))


def ask_int(label, field):
    print_hint(field)
    return int(input(label))


def main():

    print("\n🇨🇦 Canada Financial Engine — Interactive CLI\n")

    initial_savings = ask_float("Initial savings: ", "initial_savings")
    one_time_cost = ask_float("One-time migration cost: ", "one_time_cost")

    months_without_income = ask_int(
        "Months without income: ",
        "months_without_income"
    )

    monthly_income = ask_float("Expected monthly income: ", "monthly_income")

    monthly_expenses = ask_float("Monthly expenses: ", "monthly_expenses")

    savings_goal = ask_float("Savings goal: ", "savings_goal")

    inputs = FinancialInputs(
        initial_savings=initial_savings,
        one_time_cost=one_time_cost,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        months=12,
        savings_goal=savings_goal,
        months_without_income=months_without_income,
    )

    pipeline = SimulationPipeline()

    print("\n⚙️ Running simulation...\n")

    output = pipeline.run(inputs)

    projection = output["projection"]
    score = output["score"]
    risk = output["risk"]
    insights = output["insights"]

    print("\n📊 SIMULATION RESULT\n")

    print(f"Final balance: {projection.final_balance:.2f} CAD")
    print(f"Max negative balance: {projection.max_negative_balance:.2f} CAD")
    print(f"Average monthly cashflow: {projection.average_cashflow:.2f} CAD")

    print("\n🧠 FINANCIAL HEALTH")

    print(f"Score: {score['total_score']}/100")
    print(f"Interpretation: {score['interpretation']}")

    print("\n⚠️ RISK ANALYSIS")

    print(f"Risk score: {risk['risk_score']}/100")
    print(f"Risk level: {risk['risk_level']}")

    print("\n💡 INSIGHTS")

    for insight in insights:
        print(f"- {insight}")

    print("\n✅ Simulation completed.\n")


if __name__ == "__main__":
    main()