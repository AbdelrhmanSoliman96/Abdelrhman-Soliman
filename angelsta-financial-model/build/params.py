# Single source of truth for Angelsta pricing, shared by the Word doc and the Excel model.
YEARS = [2027, 2028, 2029, 2030, 2031]

# List prices in USD (GCC list). monthly = billed month to month; annual = per month when billed yearly.
STARTUP = {
    "Free":   {"monthly": [0]*5,                      "annual": [0]*5},
    "Pro":    {"monthly": [59, 59, 65, 69, 75],       "annual": [49, 49, 54, 57, 62]},
    "Team":   {"monthly": [149, 149, 159, 169, 179],  "annual": [124, 124, 132, 140, 149]},
    "Custom": {"monthly": [479, 499, 539, 575, 609],  "annual": [399, 420, 450, 480, 510]},  # avg contract
}
INVESTOR = {
    "Free":          {"monthly": [0]*5,                        "annual": [0]*5},
    "Angel":         {"monthly": [79, 79, 85, 89, 95],         "annual": [65, 65, 70, 74, 79]},
    "Institutional": {"monthly": [599, 599, 649, 679, 719],    "annual": [499, 499, 539, 565, 599]},
    "Custom":        {"monthly": [1799, 1919, 2039, 2159, 2279], "annual": [1499, 1599, 1699, 1799, 1899]},
}
INST_EXTRA_SEAT = 49        # per seat per month above 5 included seats
INST_EXTRA_PORTCO = 10      # per portfolio company per month above 50 included
EGYPT_PRICE_INDEX = 0.60    # Egypt price list as a share of the GCC list
ANNUAL_DISCOUNT_TEXT = "about 17 per cent, two months free"
PRICE_REALIZATION = [0.85, 0.92, 0.95, 0.96, 0.96]   # after founding-member and negotiated discounts
ANNUAL_SHARE_SELF = [0.25, 0.30, 0.35, 0.38, 0.40]
ANNUAL_SHARE_SALES = [0.70, 0.75, 0.80, 0.80, 0.80]
EGYPT_SHARE = [0.55, 0.40, 0.30, 0.25, 0.22]

# AI credit allowance per month by plan (fair use) and modelled average use
AI_ALLOW = {"S-Free": 25, "S-Pro": 300, "S-Team": 1500, "S-Custom": 4000,
            "I-Free": 25, "I-Angel": 500, "I-Inst": 3000, "I-Custom": 8000}
AI_USE = {"Free": 8, "S-Pro": 120, "S-Team": 500, "S-Custom": 1500,
          "I-Angel": 150, "I-Inst": 1200, "I-Custom": 3500}
AI_COST_PER_CREDIT = [0.012, 0.010, 0.008, 0.007, 0.006]

# Geography: key, label, share of paying accounts Y1..Y5, price index vs list, month the market opens
GEO = [
    ("g_egy", "Egypt, home market, EGP price list", [0.50, 0.32, 0.24, 0.20, 0.18], 0.60, 1),
    ("g_qat", "Qatar, second market", [0.15, 0.14, 0.12, 0.11, 0.10], 1.00, 4),
    ("g_ksa", "Saudi Arabia", [0.05, 0.16, 0.20, 0.21, 0.22], 1.00, 10),
    ("g_uae", "United Arab Emirates", [0.00, 0.12, 0.15, 0.16, 0.16], 1.00, 13),
    ("g_gcc", "Kuwait, Bahrain and Oman", [0.00, 0.04, 0.07, 0.08, 0.09], 1.00, 19),
    ("g_mea", "Rest of MENA and Africa, self serve", [0.18, 0.12, 0.11, 0.12, 0.12], 0.70, 1),
    ("g_row", "Rest of the world, self serve", [0.12, 0.10, 0.11, 0.12, 0.13], 1.00, 1),
]
