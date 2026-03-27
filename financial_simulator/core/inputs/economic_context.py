# financial_simulator/core/inputs/economic_context.py

class EconomicContext:
    def __init__(
        self,
        province: str | None = None,
        province_data: dict | None = None,
        all_provinces_data: dict | None = None,
    ):
        self.province = province
        self.province_data = province_data
        self.all_provinces_data = all_provinces_data