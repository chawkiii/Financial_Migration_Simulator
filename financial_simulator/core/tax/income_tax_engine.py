# financial_simulator/core/tax/income_tax_engine.py

from functools import lru_cache


class IncomeTaxEngine:

    def __init__(self, province_data: dict, payroll_data: dict):
        self.data = province_data
        self.payroll_data = payroll_data

    # =========================
    # CORE LOGIC
    # =========================
    def _calculate_progressive_tax(self, income: float, tax_config: dict) -> float:
        if income <= 0:
            return 0.0

        tax = 0.0
        previous_limit = 0.0

        for bracket in tax_config["brackets"]:

            if "up_to" in bracket:
                upper = bracket["up_to"]
                rate = bracket["rate"]

                taxable = min(income, upper) - previous_limit
                if taxable > 0:
                    tax += taxable * rate

                previous_limit = upper

            elif "above" in bracket:
                threshold = bracket["above"]
                rate = bracket["rate"]

                if income > threshold:
                    tax += (income - threshold) * rate

        return tax

    # =========================
    # INCOME TAX
    # =========================
    @lru_cache(maxsize=256)
    def calculate_income_tax(self, income: float, period: str = "annual"):

        original_income = income

        if period == "monthly":
            income *= 12

        federal = self._calculate_progressive_tax(
            income,
            self.data["income_tax"]["federal"]
        )

        provincial = self._calculate_progressive_tax(
            income,
            self.data["income_tax"]["provincial"]
        )

        if period == "monthly":
            federal /= 12
            provincial /= 12

        total = federal + provincial

        return {
            "federal_tax": federal,
            "provincial_tax": provincial,
            "total_tax": total,
            "effective_rate": total / original_income if original_income > 0 else 0
        }

    # =========================
    # PAYROLL
    # =========================
    def calculate_payroll(self, income: float, period: str = "annual"):

        if income <= 0:
            return {"total": 0.0}

        if period == "monthly":
            income *= 12

        total = 0.0
        details = {}

        # CPP / QPP
        for system in ["cpp", "qpp"]:
            config = self.payroll_data.get(system, {})
            if not config.get("enabled"):
                continue

            base_income = max(0, income - config.get("basic_exemption", 0))
            contribution = 0.0

            for rate in config.get("rates", []):
                limit = rate["up_to"]
                r = rate["rate"]

                taxable = min(base_income, limit)
                contribution += taxable * r

            total += contribution
            details[system] = contribution

        # EI / QPIP
        for system in ["ei", "qpip"]:
            config = self.payroll_data.get(system, {})
            if not config.get("enabled"):
                continue

            insurable = min(income, config.get("max_insurable_earnings", income))
            contribution = insurable * config["rate"]

            total += contribution
            details[system] = contribution

        if period == "monthly":
            for k in details:
                details[k] /= 12
            total /= 12

        details["total"] = total
        return details

    # =========================
    # NET INCOME
    # =========================
    def calculate_net_income(self, income: float, period: str = "monthly"):

        if income <= 0:
            return {
                "gross_income": income,
                "net_income": income,
                "total_deductions": 0.0,
                "effective_rate": 0.0
            }

        income_tax = self.calculate_income_tax(income, period)
        payroll = self.calculate_payroll(income, period)

        total_deductions = income_tax["total_tax"] + payroll["total"]
        net_income = income - total_deductions

        return {
            "gross_income": income,
            "net_income": net_income,
            "income_tax": income_tax,
            "payroll": payroll,
            "total_deductions": total_deductions,
            "effective_rate": total_deductions / income
        }