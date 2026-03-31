"""
Project 3 – simulate_nhex_data.py
Builds a representative health expenditure dataset
from published CIHI NHEX figures (2015–2024).
Real data: https://www.cihi.ca/en/national-health-expenditure-trends
"""

import pandas as pd
import numpy as np

np.random.seed(3)

PROVINCES = ["BC","AB","SK","MB","ON","QC","NB","NS","PE","NL"]

# Per-capita total health spending ($CAD) — 2023 actuals
# Source: CIHI NHEX 2024 Table B.1.3
PER_CAPITA_2023 = {
    "BC":9420,"AB":9870,"SK":9640,"MB":9560,"ON":9210,
    "QC":8640,"NB":9880,"NS":9740,"PE":9320,"NL":10240,
}

# Spending by category as % of total — national 2023
# Source: CIHI NHEX Table C.1.2
CATEGORIES = {
    "Hospitals":       0.263,
    "Physician Svcs":  0.130,
    "Drugs":           0.152,
    "Other Inst.":     0.096,
    "Capital":         0.041,
    "Public Health":   0.059,
    "Admin":           0.031,
    "Other":           0.228,
}

# Annual spending growth rates by category
GROWTH = {
    "Hospitals":      0.052,
    "Physician Svcs": 0.065,
    "Drugs":          0.038,
    "Other Inst.":    0.044,
    "Capital":        0.028,
    "Public Health":  0.042,
    "Admin":          0.031,
    "Other":          0.039,
}

# Drug sub-categories
DRUG_CATS = {
    "Specialty Biologics": {"share_2023": 0.28, "growth": 0.072},
    "Generic Drugs":       {"share_2023": 0.21, "growth": 0.015},
    "Brand Name Drugs":    {"share_2023": 0.24, "growth": 0.028},
    "OTC & Other":         {"share_2023": 0.15, "growth": 0.022},
    "GLP-1 Analogues":     {"share_2023": 0.12, "growth": 0.145},
}

YEARS = list(range(2015, 2025))

# ── Main spending table ───────────────────────────────────────────────────────
rows = []
for prov in PROVINCES:
    pc_2023 = PER_CAPITA_2023[prov]
    for year in YEARS:
        years_back = 2023 - year
        for cat, share in CATEGORIES.items():
            growth = GROWTH[cat]
            pc_year = (pc_2023 * share) / ((1 + growth) ** years_back)
            pc_year += np.random.normal(0, 15)
            rows.append({
                "year":          year,
                "province":      prov,
                "category":      cat,
                "per_capita_cad": max(50, round(pc_year, 0)),
                "is_forecast":   year >= 2024,
                "public_share":  round(0.70 + np.random.normal(0, 0.02), 2),
            })

df = pd.DataFrame(rows)
df.to_csv("nhex_combined.csv", index=False)
print(f"Created nhex_combined.csv  —  {len(df):,} rows")

# ── Drug sub-category table ───────────────────────────────────────────────────
drug_rows = []
for year in YEARS:
    for cat, info in DRUG_CATS.items():
        yb = 2023 - year
        share_y = info["share_2023"] / ((1 + info["growth"]) ** yb)
        share_y += np.random.normal(0, 0.005)
        drug_rows.append({
            "year":           year,
            "drug_category":  cat,
            "share_of_drug_spend": max(0.02, round(share_y, 3)),
            "annual_growth_pct":   round(info["growth"] * 100, 1),
        })

drug_df = pd.DataFrame(drug_rows)
drug_df.to_csv("nhex_drug_detail.csv", index=False)
print(f"Created nhex_drug_detail.csv  —  {len(drug_df):,} rows")
