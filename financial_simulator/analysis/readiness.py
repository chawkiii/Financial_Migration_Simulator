# financial_simulator/analysis/readiness.py

class MigrationReadinessIndex:
    """Calculates an overall readiness index for immigration based on financial, risk, and Monte Carlo results."""

    def calculate(self, result, score, risk, monte_carlo=None) -> dict:
        readiness = 0

        # Financial score weight: 40%
        readiness += score.get("total_score", 0) * 0.4

        # Cushion weight: 20%
        cushion_score = min(result.min_cushion * 12, 100)
        readiness += cushion_score * 0.2

        # Risk weight: 20% (inverse)
        risk_score = 100 - risk.get("risk_score", 0)
        readiness += risk_score * 0.2

        # Monte Carlo success weight: 20%
        if monte_carlo:
            readiness += monte_carlo.success_rate * 100 * 0.2
        else:
            readiness += 50 * 0.2  # Default neutral value

        readiness = min(readiness, 100)

        return {
            "readiness_score": round(readiness, 2),
            "level": self._interpret(readiness)
        }

    def _interpret(self, score: float) -> str:
        if score >= 80:
            return "Ready to immigrate"
        elif score >= 60:
            return "Moderately ready"
        elif score >= 40:
            return "Preparation needed"
        else:
            return "High risk immigration attempt"