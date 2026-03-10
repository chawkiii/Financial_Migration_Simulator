# financial_simulator/analysis/diagnostics.py

class FinancialDiagnostics:

    @staticmethod
    def interpret_score(total_score: int) -> str:

        if total_score >= 80:
            return "Excellent"
        elif total_score >= 60:
            return "Stable"
        elif total_score >= 40:
            return "Fragile"
        else:
            return "High Risk"

    @staticmethod
    def generate_messages(score: dict) -> list[str]:

        messages = []

        if score["survival"] == 0:
            messages.append("Your emergency savings are insufficient.")

        if score["margin"] == 0:
            messages.append("Your monthly expenses exceed your income.")

        if score["growth"] == 0:
            messages.append("Your financial situation is not improving.")

        if score["cushion"] <= 5:
            messages.append("Your financial safety cushion is critically low.")
        elif score["cushion"] <= 10:
            messages.append("Your financial cushion could be improved.")

        if score["goal"] == 0:
            messages.append("Your savings goal is not reachable within the timeframe.")

        if not messages:
            messages.append("Your financial profile looks healthy.")

        return messages

    @staticmethod
    def build_diagnosis(score: dict) -> dict:

        level = FinancialDiagnostics.interpret_score(score["total_score"])

        messages = FinancialDiagnostics.generate_messages(score)

        return {
            "level": level,
            "messages": messages
        }