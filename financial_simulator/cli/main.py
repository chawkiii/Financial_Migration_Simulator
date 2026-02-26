from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.core.scoring import FinancialScorer


def main():
    inputs = FinancialInputs(
        initial_savings=4000,
        one_time_cost=2000,
        monthly_income=3000,
        monthly_expenses=2200,
        months=12,
        savings_goal=20000,
        months_without_income=2,
    )

    print("Inputs successfully created!")
    print(vars(inputs))

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    # Gestion insolvabilité initiale
    if result.insolvent_before_income:
        print("\n⚠️ You do NOT have enough savings to survive the months without income.")

        choice = input("Do you want to continue simulation anyway? (y/n): ")

        if choice.lower() == "y":
            result = engine.simulate(force=True)
        else:
            print("Simulation stopped.")
            return

    print("\n--- Simulation Summary ---")
    print("Final balance:", result.final_balance)
    print("Goal reached at month:", result.goal_reached_month)
    print("Went negative during simulation:", result.went_negative_during_simulation)
    print("Insolvent before income:", result.insolvent_before_income)

    months_needed = engine.months_to_reach_goal()
    print("\nMonths needed to reach goal:", months_needed)

    print("\nMonthly breakdown:")
    for p in result.projections:
        print(
            f"Month {p.month_number} | "
            f"Start: {p.starting_balance} | "
            f"End: {p.ending_balance}"
        )
    
    scorer = FinancialScorer(inputs)
    score = scorer.calculate(result)

    print("\n--- Financial Health Score ---")
    print(f"Total Score: {score['total_score']} / 100")
    print(f"Survival: {score['survival']} / 25")
    print(f"Margin: {score['margin']} / 20")
    print(f"Growth: {score['growth']} / 20")
    print(f"Cushion: {score['cushion']} / 20")
    print(f"Goal: {score['goal']} / 15")

    level = engine.interpret_score(score["total_score"])
    diagnosis = engine.generate_diagnosis(score)

    print(f"\nFinancial Level: {level}")

    print("\nDiagnosis:")
    for msg in diagnosis:
        print("-", msg)


if __name__ == "__main__":
    main()