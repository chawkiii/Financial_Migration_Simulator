# financial_simulator/analysis/insights.py

class FinancialInsights:

    def generate(self, result, score):

        insights = []

        if result.insolvent_before_income:
            insights.append(
                "High risk: savings may run out before securing a job."
            )

        if result.went_negative_during_simulation:
            insights.append(
                "Your finances turn negative during the projection period."
            )

        if result.min_cushion < 2:
            insights.append(
                "Very low financial cushion. Unexpected expenses could be critical."
            )

        if score["margin"] <= 15:
            insights.append(
                "Monthly financial margin is weak."
            )

        if score["growth"] >= 10:
            insights.append(
                "Strong long-term financial growth potential."
            )

        if result.goal_reached_month:
            insights.append(
                f"Savings goal reached in month {result.goal_reached_month}."
            )

        if not insights:
            insights.append(
                "Financial situation appears stable based on current parameters."
            )

        return insights