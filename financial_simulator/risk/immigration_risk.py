# financial_simulator/risk/immigration_risk.py

from financial_simulator.core.models import ProjectionResult


class ImmigrationRiskAnalyzer:

    def calculate_risk(self, result: ProjectionResult, score: dict) -> dict:

        risk = 0
        factors = {}

        # =============================
        # 1️⃣ Survival Risk
        # =============================
        survival_score = score["survival"]

        survival_risk = max(0, 25 - survival_score)
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
        stability_score = score["stability"]

        stability_risk = max(0, 15 - stability_score)
        risk += stability_risk

        factors["stability_risk"] = stability_risk

        # =============================
        # 4️⃣ Negative Balance Severity
        # =============================
        if result.max_negative_balance < 0:

            severity = abs(result.max_negative_balance)

            if severity > 5000:
                neg_risk = 15
            elif severity > 2000:
                neg_risk = 10
            else:
                neg_risk = 5
        else:
            neg_risk = 0

        risk += neg_risk
        factors["negative_balance_risk"] = neg_risk

        # =============================
        # 5️⃣ Goal Reachability
        # =============================
        if result.goal_reached_month is None:
            goal_risk = 10
        else:
            goal_risk = 0

        risk += goal_risk
        factors["goal_risk"] = goal_risk

        # =============================
        # 6️⃣ Final Cushion
        # =============================
        cushion_score = score["cushion"]

        cushion_risk = max(0, 15 - cushion_score)

        risk += cushion_risk
        factors["cushion_risk"] = cushion_risk

        risk = max(0, min(risk, 100))

        return {
            "risk_score": risk,
            "risk_level": self.interpret_risk(risk),
            "risk_factors": factors
        }

    def interpret_risk(self, risk: int) -> str:

        if risk <= 20:
            return "Low Risk"
        elif risk <= 40:
            return "Moderate Risk"
        elif risk <= 60:
            return "Elevated Risk"
        elif risk <= 80:
            return "High Risk"
        else:
            return "Critical Risk"