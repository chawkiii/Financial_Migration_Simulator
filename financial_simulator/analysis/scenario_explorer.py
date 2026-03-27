# financial_simulator/analysis/scenario_explorer.py

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.core.inputs import SimulationInputs
from financial_simulator.analysis.scoring import FinancialScorer


class MigrationScenarioExplorer:

    def explore_income_range(self, base_inputs, income_values):

        scenarios = []

        for income in income_values:

            # =========================
            # 1️⃣ Créer un nouveau FinancialProfile avec le revenu mis à jour
            # =========================
            new_profile = base_inputs.profile.__class__(
                initial_savings=base_inputs.profile.initial_savings,
                monthly_income=income,
                monthly_expenses=base_inputs.profile.monthly_expenses,
                expenses=base_inputs.profile.expenses
            )

            # Config et context restent inchangés
            inputs = SimulationInputs(
                profile=new_profile,
                config=base_inputs.config,
                context=base_inputs.context
            )

            inputs.normalize()
            inputs.validate()

            # =========================
            # 2️⃣ Exécuter la simulation
            # =========================
            engine = ProjectionEngine(inputs)
            result = engine.simulate(force=True)
        

            # =========================
            # 4️⃣ Scorer la simulation
            # =========================
            scorer = FinancialScorer(inputs)
            score = scorer.calculate(result)

            # =========================
            # 5️⃣ Enregistrer le scénario
            # =========================
            scenarios.append({
                "income": income,
                "final_balance": result.final_balance,
                "score": score["total_score"],
                "went_negative": result.went_negative_during_simulation,

                "net_income": result.avg_net_income,
                "expenses": result.avg_monthly_expenses,
                "tax_rate": result.tax_rate_effective,
                "goal_reached": bool(result.goal_reached_month),
            })

        return scenarios