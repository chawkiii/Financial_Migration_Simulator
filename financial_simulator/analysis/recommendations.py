# financial_simulator/analysis/recommendations.py

class FinancialRecommendations:

    def generate(self, inputs, result, score):

        recommendations = []

        if result.insolvent_before_income:
            recommendations.append(
                "Increase initial savings to cover the job search period."
            )

        if score["margin"] <= 5:
            recommendations.append(
                "Reduce monthly expenses or increase income."
            )

        if result.min_cushion < 2:
            recommendations.append(
                "Build a stronger emergency fund before migrating."
            )

        if score["goal"] == 0:
            recommendations.append(
                "Extend the timeline or increase savings rate."
            )

        if not recommendations:
            recommendations.append(
                "Your financial strategy appears solid."
            )

        return recommendations