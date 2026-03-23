# financial_simulator/analysis/scenario_explorer.py

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.core.inputs import SimulationInputs
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.core.tax.income_tax_engine import IncomeTaxEngine
from financial_simulator.core.tax.expense_tax_engine import ExpenseTaxEngine
from financial_simulator.data.provinces import PROVINCES_DATA, PAYROLL_DATA


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
            # 3️⃣ Calculer taxes et net income
            # =========================
            tax_summary = None

            province_key = inputs.context.province
            if province_key:
                province_data = PROVINCES_DATA[province_key]
                payroll_data = PAYROLL_DATA.get(province_key, {})

                income_tax_engine = IncomeTaxEngine(province_data, payroll_data)
                expense_tax_engine = ExpenseTaxEngine(province_data)

                net_income_data = income_tax_engine.calculate_net_income(
                    income * 12,
                    period="monthly"
                )

                expense_tax = expense_tax_engine.calculate_sales_tax(
                    inputs.profile.expenses
                )

                # Ajouter l’impôt sur les dépenses si nécessaire
                net_income = net_income_data["net_income"] - expense_tax

                tax_summary = {
                    "net_income": net_income,
                    "income_tax": net_income_data["income_tax"],
                    "payroll": net_income_data["payroll"],
                    "expense_tax": expense_tax,
                    "total_deductions": net_income_data["total_deductions"] + expense_tax,
                    "gross_income": net_income_data["gross_income"],
                    "effective_rate": (net_income_data["total_deductions"] + expense_tax) / net_income_data["gross_income"]
                                      if net_income_data["gross_income"] > 0 else 0
                }

            # =========================
            # 4️⃣ Scorer la simulation
            # =========================
            scorer = FinancialScorer(inputs, tax_summary)
            score = scorer.calculate(result)

            # =========================
            # 5️⃣ Enregistrer le scénario
            # =========================
            scenarios.append({
                "income": income,
                "final_balance": result.final_balance,
                "score": score["total_score"],
                "went_negative": result.went_negative_during_simulation
            })

        return scenarios