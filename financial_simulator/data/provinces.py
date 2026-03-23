# financial_simulator/data/provinces.py

# -------------------------
# HELPER FUNCTION
# -------------------------

def get_payroll_config(province):
    profile = PROVINCES_DATA[province]["payroll_profile"]
    return PAYROLL_DATA[profile]

PAYROLL_DATA = {
    "canada": {
        "system": "cpp",
        "cpp": {
            "enabled": True,
            "type": "progressive",
            "basic_exemption": 3500,
            "rates": [
                {
                    "up_to": 68500,
                    "rate": 0.0595,
                    "max_contribution": 3867.50
                },
                {
                    "up_to": 73200,
                    "rate": 0.04,
                    "max_contribution": 188.00
                }
            ],
            "max_total_contribution": 4055.50
        },
        
        "ei": {
            "enabled": True,
            "type": "flat",
            "rate": 0.0166,
            "max_insurable_earnings": 63200,
            "max_contribution": 1048.72
        }
    },
    "quebec": {
        "system": "qpp",
        "qpp": {
            "enabled": True,
            "type": "progressive",
            "basic_exemption": 3500,
            "rates": [
                {
                    "up_to": 68500,
                    "rate": 0.064,
                    "max_contribution": 4160.00
                },
                {
                    "up_to": 73200,
                    "rate": 0.04,
                    "max_contribution": 188.00
                }
            ],
            "max_total_contribution": 4348.00
        },

        "ei": {
            "enabled": True,
            "type": "flat",
            "rate": 0.0132,
            "max_insurable_earnings": 63200,
            "max_contribution": 834.24
        },

        "qpip": {
            "enabled": True,
            "type": "flat",
            "rate": 0.00494,
            "max_insurable_earnings": 91000,
            "max_contribution": 449.54
        }
    }
}


PROVINCES_DATA = {

    "alberta": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "alberta",
                "type": "progressive",
                "brackets": [
                    {"up_to": 61200, "rate": 0.08},
                    {"up_to": 154259, "rate": 0.10},
                    {"up_to": 185111, "rate": 0.12},
                    {"up_to": 246813, "rate": 0.13},
                    {"up_to": 370220, "rate": 0.14},
                    {"above": 370220, "rate": 0.14}
                ],
                "max_marginal_rate": 0.14
            }
        },

        # =========================
        # SALES TAX (CONSUMPTION)
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.00,
            "hst": 0.00,
            "combined_rate": 0.05,

            # Catégories élargies pour moteur intelligent
            "category_rules": {
                "groceries": 0.05,
                "restaurant": 0.05,
                "takeout": 0.05,
                "transport": 0.05,
                "fuel": 0.05,
                "phone": 0.05,
                "internet": 0.05,
                "utilities": 0.05,
                "insurance": 0.05,
                "gym": 0.05,
                "entertainment": 0.05,
                "subscriptions": 0.05,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "ontario": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "ontario",
                "type": "progressive",
                "brackets": [
                    {"up_to": 51446, "rate": 0.0505},
                    {"up_to": 102894, "rate": 0.0915},
                    {"up_to": 150000, "rate": 0.1116},
                    {"up_to": 220000, "rate": 0.1216},
                    {"above": 220000, "rate": 0.1316}
                ],
                "max_marginal_rate": 0.1316
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.00,
            "pst": 0.00,
            "hst": 0.13,  # Ontario = HST
            "combined_rate": 0.13,

            "category_rules": {
                "groceries": 0.00,      # essentials largely exempt
                "restaurant": 0.13,
                "takeout": 0.13,
                "transport": 0.13,
                "fuel": 0.13,
                "phone": 0.13,
                "internet": 0.13,
                "utilities": 0.13,
                "insurance": 0.00,
                "gym": 0.13,
                "entertainment": 0.13,
                "subscriptions": 0.13,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "quebec": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "quebec",
                "type": "progressive",
                "brackets": [
                    {"up_to": 49275, "rate": 0.14},
                    {"up_to": 98540, "rate": 0.19},
                    {"up_to": 119910, "rate": 0.24},
                    {"above": 119910, "rate": 0.2575}
                ],
                "max_marginal_rate": 0.2575
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.09975,   # QST
            "hst": 0.00,
            "combined_rate": 0.14975,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.14975,
                "takeout": 0.14975,
                "transport": 0.14975,
                "fuel": 0.14975,
                "phone": 0.14975,
                "internet": 0.14975,
                "utilities": 0.14975,
                "insurance": 0.00,
                "gym": 0.14975,
                "entertainment": 0.14975,
                "subscriptions": 0.14975,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "quebec"
    },

    "british_columbia": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "british_columbia",
                "type": "progressive",
                "brackets": [
                    {"up_to": 47937, "rate": 0.0506},
                    {"up_to": 95875, "rate": 0.077},
                    {"up_to": 110076, "rate": 0.105},
                    {"up_to": 133664, "rate": 0.1229},
                    {"up_to": 181232, "rate": 0.147},
                    {"up_to": 252752, "rate": 0.168},
                    {"above": 252752, "rate": 0.205}
                ],
                "max_marginal_rate": 0.205
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.07,
            "hst": 0.00,
            "combined_rate": 0.12,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.12,
                "takeout": 0.12,
                "transport": 0.12,
                "fuel": 0.12,
                "phone": 0.12,
                "internet": 0.12,
                "utilities": 0.12,
                "insurance": 0.00,
                "gym": 0.12,
                "entertainment": 0.12,
                "subscriptions": 0.12,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "manitoba": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "manitoba",
                "type": "progressive",
                "brackets": [
                    {"up_to": 36150, "rate": 0.108},
                    {"up_to": 78950, "rate": 0.1275},
                    {"above": 78950, "rate": 0.174}
                ],
                "max_marginal_rate": 0.174
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.07,
            "hst": 0.00,
            "combined_rate": 0.12,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.12,
                "takeout": 0.12,
                "transport": 0.12,
                "fuel": 0.12,
                "phone": 0.12,
                "internet": 0.12,
                "utilities": 0.12,
                "insurance": 0.00,
                "gym": 0.12,
                "entertainment": 0.12,
                "subscriptions": 0.12,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "saskatchewan": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "saskatchewan",
                "type": "progressive",
                "brackets": [
                    {"up_to": 52057, "rate": 0.105},
                    {"up_to": 148734, "rate": 0.125},
                    {"above": 148734, "rate": 0.145}
                ],
                "max_marginal_rate": 0.145
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.06,
            "hst": 0.00,
            "combined_rate": 0.11,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.11,
                "takeout": 0.11,
                "transport": 0.11,
                "fuel": 0.11,
                "phone": 0.11,
                "internet": 0.11,
                "utilities": 0.11,
                "insurance": 0.00,
                "gym": 0.11,
                "entertainment": 0.11,
                "subscriptions": 0.11,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "nova_scotia": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "nova_scotia",
                "type": "progressive",
                "brackets": [
                    {"up_to": 29590, "rate": 0.0879},
                    {"up_to": 59180, "rate": 0.1495},
                    {"up_to": 93000, "rate": 0.1667},
                    {"up_to": 150000, "rate": 0.175},
                    {"above": 150000, "rate": 0.21}
                ],
                "max_marginal_rate": 0.21
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.00,
            "hst": 0.15,
            "combined_rate": 0.15,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.15,
                "takeout": 0.15,
                "transport": 0.15,
                "fuel": 0.15,
                "phone": 0.15,
                "internet": 0.15,
                "utilities": 0.15,
                "insurance": 0.00,
                "gym": 0.15,
                "entertainment": 0.15,
                "subscriptions": 0.15,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "new_brunswick": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "new_brunswick",
                "type": "progressive",
                "brackets": [
                    {"up_to": 49958, "rate": 0.094},
                    {"up_to": 99916, "rate": 0.14},
                    {"up_to": 185064, "rate": 0.16},
                    {"above": 185064, "rate": 0.195}
                ],
                "max_marginal_rate": 0.195
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.00,
            "pst": 0.00,
            "hst": 0.15,
            "combined_rate": 0.15,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.15,
                "takeout": 0.15,
                "transport": 0.15,
                "fuel": 0.15,
                "phone": 0.15,
                "internet": 0.15,
                "utilities": 0.15,
                "insurance": 0.00,
                "gym": 0.15,
                "entertainment": 0.15,
                "subscriptions": 0.15,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "newfoundland_and_labrador": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "newfoundland_and_labrador",
                "type": "progressive",
                "brackets": [
                    {"up_to": 44192, "rate": 0.087},
                    {"up_to": 88385, "rate": 0.145},
                    {"up_to": 157792, "rate": 0.158},
                    {"up_to": 220910, "rate": 0.173},
                    {"up_to": 282214, "rate": 0.183},
                    {"above": 282214, "rate": 0.218}
                ],
                "max_marginal_rate": 0.218
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.00,
            "pst": 0.00,
            "hst": 0.15,
            "combined_rate": 0.15,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.15,
                "takeout": 0.15,
                "transport": 0.15,
                "fuel": 0.15,
                "phone": 0.15,
                "internet": 0.15,
                "utilities": 0.15,
                "insurance": 0.00,
                "gym": 0.15,
                "entertainment": 0.15,
                "subscriptions": 0.15,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "prince_edward_island": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "prince_edward_island",
                "type": "progressive",
                "brackets": [
                    {"up_to": 31984, "rate": 0.098},
                    {"up_to": 63969, "rate": 0.138},
                    {"up_to": 105000, "rate": 0.167},
                    {"up_to": 140000, "rate": 0.176},
                    {"above": 140000, "rate": 0.19}
                ],
                "max_marginal_rate": 0.19
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.00,
            "pst": 0.00,
            "hst": 0.15,
            "combined_rate": 0.15,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.15,
                "takeout": 0.15,
                "transport": 0.15,
                "fuel": 0.15,
                "phone": 0.15,
                "internet": 0.15,
                "utilities": 0.15,
                "insurance": 0.00,
                "gym": 0.15,
                "entertainment": 0.15,
                "subscriptions": 0.15,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "yukon": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "yukon",
                "type": "progressive",
                "brackets": [
                    {"up_to": 55867, "rate": 0.064},
                    {"up_to": 111733, "rate": 0.09},
                    {"up_to": 173205, "rate": 0.109},
                    {"up_to": 500000, "rate": 0.128},
                    {"above": 500000, "rate": 0.15}
                ],
                "max_marginal_rate": 0.15
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.00,
            "hst": 0.00,
            "combined_rate": 0.05,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.05,
                "takeout": 0.05,
                "transport": 0.05,
                "fuel": 0.05,
                "phone": 0.05,
                "internet": 0.05,
                "utilities": 0.05,
                "insurance": 0.00,
                "gym": 0.05,
                "entertainment": 0.05,
                "subscriptions": 0.05,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "northwest_territories": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "northwest_territories",
                "type": "progressive",
                "brackets": [
                    {"up_to": 50597, "rate": 0.059},
                    {"up_to": 101198, "rate": 0.086},
                    {"up_to": 164525, "rate": 0.122},
                    {"above": 164525, "rate": 0.1405}
                ],
                "max_marginal_rate": 0.1405
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.00,
            "hst": 0.00,
            "combined_rate": 0.05,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.05,
                "takeout": 0.05,
                "transport": 0.05,
                "fuel": 0.05,
                "phone": 0.05,
                "internet": 0.05,
                "utilities": 0.05,
                "insurance": 0.00,
                "gym": 0.05,
                "entertainment": 0.05,
                "subscriptions": 0.05,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    },

    "nunavut": {

        # =========================
        # METADATA
        # =========================
        "metadata": {
            "tax_year": 2026,
            "effective_from": "2026-01-01",
            "last_updated": "2026-03-16",
            "data_source": "manual_curated",
            "version": "1.0"
        },

        # =========================
        # INCOME TAX
        # =========================
        "income_tax": {

            "federal": {
                "type": "progressive",
                "brackets": [
                    {"up_to": 58523, "rate": 0.14},
                    {"up_to": 117045, "rate": 0.205},
                    {"up_to": 181440, "rate": 0.26},
                    {"up_to": 258482, "rate": 0.29},
                    {"up_to": 640600, "rate": 0.33},
                    {"above": 640600, "rate": 0.37}
                ],
                "max_marginal_rate": 0.37
            },

            "provincial": {
                "province": "nunavut",
                "type": "progressive",
                "brackets": [
                    {"up_to": 53268, "rate": 0.04},
                    {"up_to": 106537, "rate": 0.07},
                    {"up_to": 173205, "rate": 0.09},
                    {"above": 173205, "rate": 0.115}
                ],
                "max_marginal_rate": 0.115
            }
        },

        # =========================
        # SALES TAX
        # =========================
        "expense_tax": {

            "gst": 0.05,
            "pst": 0.00,
            "hst": 0.00,
            "combined_rate": 0.05,

            "category_rules": {
                "groceries": 0.00,
                "restaurant": 0.05,
                "takeout": 0.05,
                "transport": 0.05,
                "fuel": 0.05,
                "phone": 0.05,
                "internet": 0.05,
                "utilities": 0.05,
                "insurance": 0.00,
                "gym": 0.05,
                "entertainment": 0.05,
                "subscriptions": 0.05,
                "rent": 0.00
            }
        },
        # =========================
        # PAYROLL REFERENCE
        # =========================
        "payroll_profile": "canada"
    }

}

