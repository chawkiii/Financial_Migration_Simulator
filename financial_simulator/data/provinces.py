# financial_simulator/data/provinces.py

PROVINCES_DATA = {

    "ontario": {
        "average_rent": 2150,   # moyenne provinciale ~1870-2330 CAD
        "tax_rate": 0.295,      # revenu moyen combiné ~29-30%
        "cost_of_living_index": 1.25,
        "job_market_score": 82
    },

    "quebec": {
        "average_rent": 1620,   # moyenne provinciale ~1520-1960 CAD
        "tax_rate": 0.37,       # province la plus taxée
        "cost_of_living_index": 1.05,
        "job_market_score": 72
    },

    "alberta": {
        "average_rent": 1750,   # ~1700-1860 CAD
        "tax_rate": 0.25,       # flat provincial tax faible
        "cost_of_living_index": 1.00,
        "job_market_score": 85
    },

    "british_columbia": {
        "average_rent": 2460,   # province la plus chère
        "tax_rate": 0.28,
        "cost_of_living_index": 1.35,
        "job_market_score": 78
    }
}


def get_province(name: str):

    name = name.lower()

    if name not in PROVINCES_DATA:
        raise ValueError("Province not supported")

    return PROVINCES_DATA[name]