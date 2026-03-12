# financial_simulator/data/provinces.py

PROVINCES_DATA = {

    "ontario": {
        "average_rent": 1800,
        "tax_rate": 0.30,
        "cost_of_living_index": 1.2,
        "job_market_score": 70
    },

    "quebec": {
        "average_rent": 1500,
        "tax_rate": 0.34,
        "cost_of_living_index": 1.1,
        "job_market_score": 65
    },

    "alberta": {
        "average_rent": 1400,
        "tax_rate": 0.25,
        "cost_of_living_index": 1.0,
        "job_market_score": 75
    },

    "british_columbia": {
        "average_rent": 2000,
        "tax_rate": 0.29,
        "cost_of_living_index": 1.3,
        "job_market_score": 68
    }
}


def get_province(name: str):

    name = name.lower()

    if name not in PROVINCES_DATA:
        raise ValueError("Province not supported")

    return PROVINCES_DATA[name]