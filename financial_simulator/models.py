class MonthlyProjection:
    def __init__(
        self,
        month_number: int,
        starting_balance: float,
        net_cashflow: float,
        ending_balance: float,
    ):
        self.month_number = month_number
        self.starting_balance = starting_balance
        self.net_cashflow = net_cashflow
        self.ending_balance = ending_balance


class ProjectionResult:
    def __init__(
        self,
        projections: list,
        final_balance: float,
        goal_reached_month: int | None,
        went_negative_during_simulation: bool,
        insolvent_before_income: bool,
    ):
        self.projections = projections
        self.final_balance = final_balance
        self.goal_reached_month = goal_reached_month
        self.went_negative_during_simulation = went_negative_during_simulation
        self.insolvent_before_income = insolvent_before_income