# financial_simulator/cli/main_interactive.py
from financial_simulator.core.inputs import FinancialInputs
from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.core.hints import FIELD_HINTS
from financial_simulator.analysis.diagnostics import FinancialDiagnostics

def print_hint(field_name):
    hint = FIELD_HINTS.get(field_name)
    if hint:
        print(f"💡 Hint: {hint}")

def main():
    print("Bienvenue dans la CLI Interactive\n")

    print_hint("initial_savings")
    initial_savings = float(input("Initial savings: "))

    print_hint("one_time_cost")
    one_time_cost = float(input("One-time cost: "))

    print_hint("months_without_income")
    months_without_income = int(input("Months without income: "))

    print_hint("monthly_income")
    monthly_income = float(input("Monthly income: "))

    print_hint("monthly_expenses")
    monthly_expenses = float(input("Monthly expenses: "))

    print_hint("savings_goal")
    savings_goal = float(input("Savings goal: "))

    inputs = FinancialInputs(
        initial_savings=initial_savings,
        one_time_cost=one_time_cost,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        months=12,  
        savings_goal=savings_goal,
        months_without_income=months_without_income,
    )

    print("\n✨ Inputs successfully created!")
    print(vars(inputs))

    engine = ProjectionEngine(inputs)
    result = engine.simulate()

    if result.insolvent_before_income:
        print("\n⚠️ Attention : fonds insuffisants pour survivre les mois sans revenu.")
        choice = input("Voulez-vous continuer la simulation quand même ? (y/n): ")
        if choice.lower() == "y":
            result = engine.simulate(force=True)
        else:
            print("Simulation stoppée.")
            return

    print("\n--- Résumé de la simulation ---")
    print(f"Final balance: {result.final_balance}")
    print(f"Goal reached at month: {result.goal_reached_month}")
    print(f"Went negative: {result.went_negative_during_simulation}")
    print(f"Insolvent before income: {result.insolvent_before_income}")

    scorer = FinancialScorer(inputs)
    score = scorer.calculate(result)

    print("\n--- Financial Health Score ---")
    print(f"Total Score: {score['total_score']} / 100")
    print(f"Survival: {score['survival']} / 25")
    print(f"Margin: {score['margin']} / 20")
    print(f"Stability: {score['stability']} / 15")
    print(f"Growth: {score['growth']} / 15")
    print(f"Cushion: {score['cushion']} / 15")
    print(f"Goal: {score['goal']} / 10")

    diagnosis = FinancialDiagnostics.build_diagnosis(score)

    level = diagnosis["level"]
    messages = diagnosis["messages"]

    print(f"\nFinancial Level: {level}")

    print("\nDiagnosis:")
    for msg in messages:
        print("-", msg)

    print("\nsimulation terminée avec succès !")

if __name__ == "__main__":
    main()