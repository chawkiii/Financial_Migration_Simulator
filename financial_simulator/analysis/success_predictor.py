# financial_simulator/analysis/success_predictor.py

class ImmigrationSuccessPredictor:

    def predict(self, result, score, monte_carlo, risk):

        # =============================
        # 1️⃣ MONTE CARLO (if available)
        # =============================
        if monte_carlo:
            monte_success = monte_carlo.success_rate * 100
            monte_weight = 0.4
        else:
            monte_success = score["total_score"]  # fallback intelligent
            monte_weight = 0.2  # moins de poids si absent

        # =============================
        # 2️⃣ CORE COMPONENTS
        # =============================
        financial_score = score["total_score"]

        cushion_factor = max(0, min(result.min_cushion / 6, 1))
        cushion_score = cushion_factor * 100

        risk_factor = 1 - (risk["risk_score"] / 100)
        risk_score = risk_factor * 100

        # =============================
        # 3️⃣ FINAL WEIGHTING
        # =============================
        final_probability = (
            monte_success * monte_weight +
            financial_score * 0.3 +
            cushion_score * 0.2 +
            risk_score * 0.1
        )

        final_probability = max(0, min(final_probability, 100))

        # =============================
        # 4️⃣ CONFIDENCE LEVEL
        # =============================
        confidence = self._compute_confidence(monte_carlo)

        # =============================
        # 5️⃣ EXPLANATION
        # =============================
        explanation = self._build_explanation(
            financial_score,
            cushion_score,
            risk_score,
            monte_success,
            monte_carlo
        )

        return {
            "success_probability": round(final_probability, 2),
            "confidence": confidence,
            "explanation": explanation
        }

    # =============================
    # HELPERS
    # =============================

    def _compute_confidence(self, monte_carlo):

        if not monte_carlo:
            return "Medium"

        if monte_carlo.simulations_run >= 500:
            return "High"
        elif monte_carlo.simulations_run >= 200:
            return "Medium"
        return "Low"

    def _build_explanation(
        self,
        financial_score,
        cushion_score,
        risk_score,
        monte_success,
        monte_carlo
    ):

        explanations = []

        if financial_score >= 70:
            explanations.append("Strong financial fundamentals")
        elif financial_score < 40:
            explanations.append("Weak financial foundation")

        if cushion_score >= 70:
            explanations.append("Good financial safety buffer")
        elif cushion_score < 30:
            explanations.append("Low financial cushion")

        if risk_score >= 70:
            explanations.append("Low overall risk profile")
        elif risk_score < 40:
            explanations.append("Elevated risk level")

        if monte_carlo:
            if monte_success >= 70:
                explanations.append("High success rate across scenarios")
            elif monte_success < 40:
                explanations.append("Low success rate under uncertainty")

        return explanations