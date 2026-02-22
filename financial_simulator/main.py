from inputs import FinancialInputs
from engine import ProjectionEngine


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


if __name__ == "__main__":
    main()