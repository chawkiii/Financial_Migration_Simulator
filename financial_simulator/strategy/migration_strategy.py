# financial_simulator/strategy/migration_strategy.py

class MigrationStrategyPlanner:

    def suggest(self, inputs, result, score=None):
        """
        Generate actionable financial recommendations for immigration planning.
        Optional: include score for more context-aware advice.
        """
        strategy = []

        total_expenses = inputs.profile.get_total_expenses()
        initial_savings = inputs.profile.initial_savings - getattr(inputs, "one_time_cost", 0)

        # ==============================
        # 1️⃣ Financial Buffer (emergency savings)
        # ==============================
        recommended_buffer = total_expenses * 6
        if initial_savings < recommended_buffer:
            needed = recommended_buffer - initial_savings
            strategy.append({
                "priority": "high",
                "message": f"Increase savings by approx. ${round(needed, 2)} to reach a safer financial buffer (6 months of expenses)."
            })

        # ==============================
        # 2️⃣ Expense-to-Income Ratio
        # ==============================
        if total_expenses > inputs.profile.monthly_income * 0.8:
            strategy.append({
                "priority": "medium",
                "message": "Consider reducing monthly expenses to improve financial stability (expenses > 80% of income)."
            })

        # ==============================
        # 3️⃣ Survival Risk
        # ==============================
        if result.insolvent_before_income:
            strategy.append({
                "priority": "high",
                "message": "Initial savings insufficient to survive initial job search period. Increase cash reserves."
            })

        # ==============================
        # 4️⃣ Savings Goal Feasibility
        # ==============================
        if result.goal_reached_month is None and inputs.config.savings_goal > 0:
            strategy.append({
                "priority": "medium",
                "message": "Savings goal may be unrealistic with current financial parameters."
            })

        # ==============================
        # 5️⃣ Optional: Score-driven advice
        # ==============================
        if score:
            if score["margin"] <= 5:
                strategy.append({
                    "priority": "high",
                    "message": "Financial margin is critically low. Consider increasing income or reducing expenses."
                })

            if score["cushion"] <= 2:
                strategy.append({
                    "priority": "high",
                    "message": "Low cushion indicates vulnerability to unexpected expenses."
                })

        # ==============================
        # 6️⃣ Default fallback
        # ==============================
        if not strategy:
            strategy.append({
                "priority": "low",
                "message": "Current financial setup appears viable for immigration planning."
            })

        return strategy