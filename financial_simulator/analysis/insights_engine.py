# financial_simulator/analysis/insights_engine.py

class InsightsEngine:

    def __init__(self, inputs, projection, score, optimization=None):
        self.inputs = inputs
        self.projection = projection
        self.score = score
        self.optimization = optimization or {}

    # =============================
    # MAIN ENTRY
    # =============================
    def generate(self):

        insights = []

        insights += self._income_vs_expenses()
        insights += self._risk_analysis()
        insights += self._goal_analysis()
        insights += self._tax_analysis()
        insights += self._province_optimization()

        return insights

    # =============================
    # INSIGHT BLOCKS
    # =============================

    def _income_vs_expenses(self):

        insights = []

        net = self.projection.avg_net_income
        expenses = self.projection.avg_monthly_expenses

        if expenses == 0:
            return insights

        ratio = net / expenses

        if ratio < 1:
            insights.append({
                "type": "risk",
                "title": "Deficit Risk",
                "message": "Your expenses exceed your income. This is not sustainable.",
                "severity": "high"
            })

        elif ratio < 1.2:
            insights.append({
                "type": "warning",
                "title": "Low Financial Margin",
                "message": "Your financial margin is very tight. Consider reducing expenses.",
                "severity": "medium"
            })

        elif ratio > 1.5:
            insights.append({
                "type": "positive",
                "title": "Strong Financial Margin",
                "message": "You have a comfortable financial buffer each month.",
                "severity": "low"
            })

        return insights

    def _risk_analysis(self):

        insights = []

        if self.projection.went_negative_during_simulation:
            insights.append({
                "type": "risk",
                "title": "Cash Flow Instability",
                "message": "Your balance goes negative during the simulation.",
                "severity": "high"
            })

        return insights

    def _goal_analysis(self):

        insights = []

        if self.projection.goal_reached_month:
            insights.append({
                "type": "positive",
                "title": "Goal Achievable",
                "message": f"You can reach your goal in {self.projection.goal_reached_month} months.",
                "severity": "low"
            })
        else:
            insights.append({
                "type": "warning",
                "title": "Goal Not Reached",
                "message": "With your current setup, your goal is not reached.",
                "severity": "medium"
            })

        return insights

    def _tax_analysis(self):

        insights = []

        tax_rate = self.projection.tax_rate_effective

        if tax_rate > 0.30:
            insights.append({
                "type": "warning",
                "title": "High Tax Pressure",
                "message": "A significant portion of your income goes to taxes.",
                "severity": "medium"
            })

        return insights

    def _province_optimization(self):

        insights = []

        best = self.optimization.get("best")

        if not best:
            return insights

        current_score = self.score["total_score"]
        best_score = best["score"]

        delta = best_score - current_score

        if delta >= 10:
            insights.append({
                "type": "opportunity",
                "title": "Better Province Available",
                "message": f"You could improve your score by +{delta} by choosing {best['province']}.",
                "severity": "medium"
            })

        return insights