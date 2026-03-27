# financial_simulator/core/projection.py

from financial_simulator.core.engine import ProjectionEngine

from financial_simulator.core.tax.income_tax_engine import IncomeTaxEngine
from financial_simulator.core.tax.expense_tax_engine import ExpenseTaxEngine

from financial_simulator.data.provinces import PROVINCES_DATA, PAYROLL_DATA


def run_projection(inputs):

    # =========================
    # CONTEXT
    # =========================
    province_key = inputs.context.province.lower()
    province_data = PROVINCES_DATA[province_key]

    payroll_key = "quebec" if province_key == "quebec" else "canada"
    payroll_data = PAYROLL_DATA[payroll_key]

    # =========================
    # TAX ENGINES
    # =========================
    income_engine = IncomeTaxEngine(province_data, payroll_data)
    expense_engine = ExpenseTaxEngine(province_data)

    # =========================
    # INCOME (AFTER TAX)
    # =========================
    net_income_data = income_engine.calculate_net_income(
        inputs.profile.monthly_income,
        period="monthly"
    )

    net_income = net_income_data["net_income"]

    # =========================
    # EXPENSES
    # =========================
    if inputs.profile.expenses is not None:
        base_expenses = sum(inputs.profile.expenses.values())
        expenses_detail = inputs.profile.expenses
    else:
        base_expenses = inputs.profile.monthly_expenses
        expenses_detail = None

    # =========================
    # MONTHLY TAX HOOK
    # =========================
    def monthly_tax_hook(month, cashflow):
        sales_tax = expense_engine.calculate_sales_tax(expenses_detail)
        return cashflow - sales_tax

    # =========================
    # ENGINE (V3 ✅)
    # =========================
    engine = ProjectionEngine(inputs)

    result = engine.simulate(
        monthly_income=net_income,
        monthly_expenses=base_expenses,
        monthly_hook=monthly_tax_hook,
        force=True
    )

    # =========================
    # TAX SUMMARY
    # =========================
    tax_summary = {
        "income": net_income_data,
        "monthly_sales_tax": expense_engine.calculate_sales_tax(expenses_detail)
    }

    return result, tax_summary