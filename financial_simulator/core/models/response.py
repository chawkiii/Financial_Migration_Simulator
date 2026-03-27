# financial_simulator/core/models/response.py

class SimulationResponse:

    def __init__(
        self,
        projection,
        score,
        risk,
        success,
        readiness,
        insights,
        recommendations,
        strategy,
        scenarios,
        optimization,
        monte_carlo=None
    ):
        self.projection = projection
        self.score = score
        self.risk = risk
        self.success = success
        self.readiness = readiness
        self.insights = insights
        self.recommendations = recommendations
        self.strategy = strategy
        self.scenarios = scenarios
        self.optimization = optimization
        self.monte_carlo = monte_carlo

    def to_dict(self):

        return {
            "summary": {
                "final_balance": self.projection.final_balance,
                "goal_reached": bool(self.projection.goal_reached_month),
                "goal_month": self.projection.goal_reached_month,
            },

            "financials": {
                "net_income": self.projection.avg_net_income,
                "expenses": self.projection.avg_monthly_expenses,
                "tax_rate": self.projection.tax_rate_effective,
                "total_tax_paid": self.projection.total_tax_paid,
            },

            "risk": self.risk,
            "score": self.score,
            "success": self.success,
            "readiness": self.readiness,

            "insights": self.insights,
            "recommendations": self.recommendations,
            "strategy": self.strategy,

            "scenarios": self.scenarios,
            "optimization": self.optimization,

            "monte_carlo": (
                {
                    "success_rate": self.monte_carlo.success_rate,
                    "failure_rate": self.monte_carlo.failure_rate,
                    "worst_balance": self.monte_carlo.worst_balance,
                    "average_final_balance": self.monte_carlo.average_final_balance,
                }
                if self.monte_carlo else None
            ),
        }