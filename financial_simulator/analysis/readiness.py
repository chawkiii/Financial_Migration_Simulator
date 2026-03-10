# financial_simulator/analysis/readiness.py

class MigrationReadinessIndex:

    def calculate(self, result, score, risk, monte_carlo=None):

        readiness = 0

        # Score financier (40%)
        readiness += score["total_score"] * 0.4

        # Cushion (20%)
        cushion_score = min(result.min_cushion * 10, 100)
        readiness += cushion_score * 0.2

        # Risk (20%) (inversé)
        risk_score = 100 - risk["risk_score"]
        readiness += risk_score * 0.2

        # Monte Carlo (20%)
        if monte_carlo:
            readiness += monte_carlo.success_rate * 100 * 0.2
        else:
            readiness += 50 * 0.2

        readiness = min(readiness, 100)

        return {
            "readiness_score": round(readiness, 2),
            "level": self._interpret(readiness)
        }

    def _interpret(self, score):

        if score >= 80:
            return "Ready to immigrate"

        if score >= 60:
            return "Moderately ready"

        if score >= 40:
            return "Preparation needed"

        return "High risk immigration attempt"