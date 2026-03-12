# financial_simulator/strategy/migration_strategy.py

class MigrationStrategyPlanner:

    def suggest(self, inputs, result):

        strategy = []

        # augmenter épargne
        if inputs.initial_savings < inputs.monthly_expenses * 6:

            needed = (inputs.monthly_expenses * 6) - inputs.initial_savings

            strategy.append(
                f"Increase savings by approximately {round(needed, 2)} to reach a safer financial buffer."
            )

        # réduire dépenses
        if inputs.monthly_expenses > inputs.monthly_income * 0.8:

            strategy.append(
                "Consider reducing monthly expenses to improve financial stability."
            )

        # délai immigration
        if result.insolvent_before_income:

            strategy.append(
                "Increase savings to survive the initial job search period."
            )

        # objectif irréaliste
        if result.goal_reached_month is None and inputs.savings_goal > 0:

            strategy.append(
                "Savings goal may be unrealistic with current financial parameters."
            )

        if not strategy:

            strategy.append(
                "Current financial setup appears viable for immigration planning."
            )

        return strategy