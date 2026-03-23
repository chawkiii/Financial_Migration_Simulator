# financial_simulator/risk/immigration_risk.py

from financial_simulator.core.models import ProjectionResult


class ImmigrationRiskAnalyzer:

    def calculate_risk(self, result: ProjectionResult, score: dict) -> dict:

        risk = 0
        factors = {}

        # =============================
        # 1️⃣ Survival Risk (CRITICAL)
        # =============================
        survival_score = score["survival"]
        survival_risk = max(0, 25 - survival_score)

        if result.insolvent_before_income:
            survival_risk += 20  # 🚨 RED FLAG

        risk += survival_risk
        factors["survival_risk"] = survival_risk

        # =============================
        # 2️⃣ Margin Risk
        # =============================
        margin_score = score["margin"]
        margin_risk = max(0, 20 - margin_score)

        risk += margin_risk
        factors["margin_risk"] = margin_risk

        # =============================
        # 3️⃣ Stability Risk
        # =============================
        if result.went_negative_during_simulation:
            stability_risk = 20  # 🚨 HIGH PENALTY
        else:
            stability_risk = max(0, 15 - score["stability"])

        risk += stability_risk
        factors["stability_risk"] = stability_risk

        # =============================
        # 4️⃣ Negative Balance Severity
        # =============================
        neg_risk = 0

        if result.max_negative_balance < 0:
            severity = abs(result.max_negative_balance)

            if severity > 5000:
                neg_risk = 20
            elif severity > 2000:
                neg_risk = 15
            elif severity > 1000:
                neg_risk = 10
            else:
                neg_risk = 5

        risk += neg_risk
        factors["negative_balance_risk"] = neg_risk

        # =============================
        # 5️⃣ Goal Risk
        # =============================
        goal_risk = 0 if result.goal_reached_month else 10

        risk += goal_risk
        factors["goal_risk"] = goal_risk

        # =============================
        # 6️⃣ Cushion Risk
        # =============================
        cushion_risk = max(0, 15 - score["cushion"])

        risk += cushion_risk
        factors["cushion_risk"] = cushion_risk

        # =============================
        # NORMALIZATION
        # =============================
        risk = max(0, min(risk, 100))

        return {
            "risk_score": risk,
            "risk_level": self._interpret_risk(risk),
            "risk_factors": factors,
            "red_flags": self._detect_red_flags(result)
        }

    def _interpret_risk(self, risk: int) -> str:

        if risk <= 20:
            return "Low Risk"
        elif risk <= 40:
            return "Moderate Risk"
        elif risk <= 60:
            return "Elevated Risk"
        elif risk <= 80:
            return "High Risk"
        return "Critical Risk"

    def _detect_red_flags(self, result: ProjectionResult):

        flags = []

        if result.insolvent_before_income:
            flags.append("Insufficient savings before income starts")

        if result.went_negative_during_simulation:
            flags.append("Negative balance during simulation")

        if result.max_negative_balance < -3000:
            flags.append("Severe negative balance risk")

        return flags