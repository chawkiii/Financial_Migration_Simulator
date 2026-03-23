# financial_simulator/core/inputs/economic_context.py

class EconomicContext:
    def __init__(
        self,
        province: str | None = None,
    ):
        self.province = province