# financial_simulator/analysis/diagnostics.py

class FinancialDiagnostics:

    @staticmethod
    def interpret_score(total_score: int) -> str:

        if total_score >= 80:
            return "Excellent"
        elif total_score >= 65:
            return "Good"
        elif total_score >= 50:
            return "Moderate"
        elif total_score >= 35:
            return "High Risk"
        return "Critical"

    @staticmethod
    def generate_messages(score: dict) -> list[str]:

        messages = []

        if score.get("survival", 0) <= 5:
            messages.append("Insufficient emergency savings before income starts")

        if score.get("margin", 0) == 0:
            messages.append("Expenses exceed income → unsustainable situation")

        if score.get("stability", 0) == 0:
            messages.append("Cash flow instability detected")

        if score.get("growth", 0) == 0:
            messages.append("No financial growth observed")

        cushion = score.get("cushion", 0)

        if cushion <= 5:
            messages.append("Critical lack of financial cushion")
        elif cushion <= 10:
            messages.append("Limited financial safety buffer")

        if score.get("goal", 0) == 0:
            messages.append("Savings goal not achievable within timeframe")

        if not messages:
            messages.append("Strong financial profile with low risk indicators")

        return messages

    @staticmethod
    def build_diagnosis(score: dict) -> dict:

        return {
            "level": FinancialDiagnostics.interpret_score(score["total_score"]),
            "messages": FinancialDiagnostics.generate_messages(score)
        }