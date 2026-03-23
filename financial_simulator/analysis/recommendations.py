# financial_simulator/analysis/recommendations.py

class FinancialRecommendations:
    """Generates actionable recommendations for improving financial readiness."""

    def generate(self, inputs, result, score) -> list[str]:
        recommendations = []

        profile = inputs.profile  # ✅ accéder correctement aux attributs

        # Initial savings insufficient
        if result.insolvent_before_income:
            recommendations.append(
                "Increase initial savings to cover the job search period."
            )

        # Low monthly margin
        if score.get("margin", 0) <= 5:
            recommendations.append(
                "Reduce monthly expenses or increase income."
            )

        # Emergency fund low
        if result.min_cushion < 3:
            recommendations.append(
                "Build a stronger emergency fund before migrating."
            )

        # Unrealistic savings goal
        if score.get("goal", 0) == 0:
            recommendations.append(
                "Extend the timeline or increase savings rate to meet your goal."
            )

        # Housing expenses check
        if profile.expenses:
            rent = profile.expenses.get("rent", 0)
            if rent > profile.monthly_income * 0.4:
                recommendations.append(
                    "Housing costs are high relative to income."
                )

        # Default recommendation
        if not recommendations:
            recommendations.append(
                "Your financial strategy appears solid."
            )

        return recommendations