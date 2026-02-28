# financial_simulator/core/models.py
class MonthlyProjection:
    def __init__(self, month_number, starting_balance, net_cashflow, ending_balance):
        self.month_number = month_number
        self.starting_balance = starting_balance
        self.net_cashflow = net_cashflow
        self.ending_balance = ending_balance

    def to_dict(self):
        return {
            "month_number": self.month_number,
            "starting_balance": self.starting_balance,
            "net_cashflow": self.net_cashflow,
            "ending_balance": self.ending_balance,
        }


class ProjectionResult:
    def __init__(
        self,
        projections,
        final_balance,
        goal_reached_month,
        went_negative_during_simulation,
        insolvent_before_income,
        max_negative_balance=0,
        average_cashflow=0,
        min_cushion=0,
    ):
        self.projections = projections
        self.final_balance = final_balance
        self.goal_reached_month = goal_reached_month
        self.went_negative_during_simulation = went_negative_during_simulation
        self.insolvent_before_income = insolvent_before_income

        # NEW V2.1 fields
        self.max_negative_balance = max_negative_balance
        self.average_cashflow = average_cashflow
        self.min_cushion = min_cushion
        
    def to_dict(self):
        return {
            "final_balance": self.final_balance,
            "goal_reached_month": self.goal_reached_month,
            "went_negative_during_simulation": self.went_negative_during_simulation,
            "insolvent_before_income": self.insolvent_before_income,
            "max_negative_balance": self.max_negative_balance,
            "average_cashflow": self.average_cashflow,
            "min_cushion": self.min_cushion,
            "projections": [p.to_dict() for p in self.projections],
        }