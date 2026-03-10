# financial_simulator/scenarios/canada.py
CANADA_PROVINCES = {

    "ontario": {
        "tax_rate": 0.30,
        "average_rent": 1800,
        "cost_of_living_index": 1.2,
        "job_market_risk": 1.0
    },

    "quebec": {
        "tax_rate": 0.34,
        "average_rent": 1500,
        "cost_of_living_index": 1.1,
        "job_market_risk": 1.1
    },

    "alberta": {
        "tax_rate": 0.25,
        "average_rent": 1400,
        "cost_of_living_index": 1.0,
        "job_market_risk": 0.9
    },

    "british_columbia": {
        "tax_rate": 0.29,
        "average_rent": 2000,
        "cost_of_living_index": 1.3,
        "job_market_risk": 1.2
    }

}

def get_province_data(province: str):

    province = province.lower()

    if province not in CANADA_PROVINCES:
        raise ValueError("Province not supported")

    return CANADA_PROVINCES[province]