# financial_simulator/analysis/success_predictor.py

class ImmigrationSuccessPredictor:

    def predict(self, result, score, monte_carlo, risk):

        monte_success = monte_carlo.success_rate * 100
        financial_score = score["total_score"]

        cushion_factor = max(0, min(result.min_cushion / 6, 1))
        cushion_score = cushion_factor * 100

        risk_factor = 1 - (risk["risk_score"] / 100)
        risk_score = risk_factor * 100

        final_probability = (
            monte_success * 0.4 +
            financial_score * 0.3 +
            cushion_score * 0.2 +
            risk_score * 0.1
        )

        final_probability = max(0, min(final_probability, 100))

        return {
            "success_probability": round(final_probability, 2)
        }