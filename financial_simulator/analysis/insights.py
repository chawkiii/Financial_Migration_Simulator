# financial_simulator/analysis/insights.py

class FinancialInsights:

    def generate(self, result, score=None, monte_carlo=None):
        """
        Generate qualitative insights based on simulation results,
        score breakdown, and optional Monte Carlo analysis.
        """
        insights = []

        # ==============================
        # Critical issues first
        # ==============================
        if result.insolvent_before_income:
            insights.append("High risk: savings may run out before securing a job.")

        if result.went_negative_during_simulation:
            insights.append("Projected finances go negative during the simulation period.")

        if result.min_cushion < 2:
            insights.append("Very low financial cushion: unexpected expenses could be critical.")

        # ==============================
        # Score-driven insights
        # ==============================
        if score:
            if score.get("margin", 0) <= 10:
                insights.append("Monthly financial margin is weak.")
            if score.get("growth", 0) >= 10:
                insights.append("Strong long-term financial growth potential.")
            if score.get("goal", 0) == 0:
                insights.append("Savings goal may not be achievable in timeframe.")

        # ==============================
        # Monte Carlo insights
        # ==============================
        if monte_carlo:
            if monte_carlo.success_rate >= 0.7:
                insights.append("Monte Carlo: high probability of financial success under variability.")
            elif monte_carlo.success_rate <= 0.3:
                insights.append("Monte Carlo: high risk under income/expense uncertainty.")

        # ==============================
        # Default safe
        # ==============================
        if not insights:
            insights.append("Financial situation appears stable based on current parameters.")

        return insights