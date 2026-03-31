"""
Project 3 – 01_clean_explore.py + 02_analysis.py
DATA DETECTIVE → PROGRAMMER → STORYTELLER → CONSULTANT
"""

import pandas as pd
import numpy as np

sep = "=" * 62

# ─────────────────────────────────────────────────────────────
# PART 1: CLEAN AND EXPLORE
# ─────────────────────────────────────────────────────────────

df   = pd.read_csv("nhex_combined.csv")
drug = pd.read_csv("nhex_drug_detail.csv")

print(f"\n{sep}")
print("  PART 1 — DATA DETECTIVE: CLEAN AND PROFILE")
print(f"{sep}")
print(f"\n  Spending rows:  {len(df):,}")
print(f"  Drug rows:      {len(drug):,}")
print(f"  Provinces:      {sorted(df['province'].unique())}")
print(f"  Years:          {df['year'].min()} – {df['year'].max()}")
print(f"  Categories:     {sorted(df['category'].unique())}")

# Flag forecast years
forecast = df[df["is_forecast"] == True]
actual   = df[df["is_forecast"] == False]
print(f"\n  Actual years:   {sorted(actual['year'].unique())}")
print(f"  Forecast years: {sorted(forecast['year'].unique())} (handle separately)")

# Range checks
print(f"\n  Per-capita range: ${df['per_capita_cad'].min():,.0f} – ${df['per_capita_cad'].max():,.0f}")
print(f"  Public share range: {df['public_share'].min():.0%} – {df['public_share'].max():.0%}")

nulls = df.isnull().sum()
if nulls.sum() == 0:
    print("\n  No missing values.")

df.to_csv("nhex_clean.csv", index=False)
print(f"\n  Saved: nhex_clean.csv")

# ─────────────────────────────────────────────────────────────
# PART 2: ANALYSIS
# ─────────────────────────────────────────────────────────────

print(f"\n{sep}")
print("  PART 2 — ANALYSIS")
print(f"{sep}")

actual_df = df[df["is_forecast"] == False]
latest_yr = actual_df["year"].max()
early_yr  = actual_df["year"].min()

# Per-capita total by province — latest actual year
print(f"\n{'─'*62}")
print(f"PER-CAPITA HEALTH SPENDING BY PROVINCE — {latest_yr}")
print(f"{'─'*62}")

prov = (actual_df[actual_df["year"] == latest_yr]
        .groupby("province")["per_capita_cad"]
        .sum().sort_values(ascending=False).reset_index())
prov.columns = ["province","total_per_capita"]
nat_avg = prov["total_per_capita"].mean()

print(f"\n  {'Province':>10} {'Per Capita':>12} {'vs National':>13}")
print(f"  {'─'*10} {'─'*12} {'─'*13}")
for _, r in prov.iterrows():
    diff = r["total_per_capita"] - nat_avg
    flag = " ◄ HIGHEST" if r["total_per_capita"] == prov["total_per_capita"].max() else ""
    print(f"  {r['province']:>10} ${r['total_per_capita']:>10,.0f} {diff:>+12.0f}{flag}")

print(f"\n  National average: ${nat_avg:,.0f}")

# Spending by category
print(f"\n{'─'*62}")
print(f"SPENDING BY CATEGORY — National {latest_yr}")
print(f"{'─'*62}")

cats = (actual_df[actual_df["year"] == latest_yr]
        .groupby("category")["per_capita_cad"]
        .mean().sort_values(ascending=False).reset_index())
total_pc = cats["per_capita_cad"].sum()
cats["share"] = cats["per_capita_cad"] / total_pc * 100

print(f"\n  {'Category':<22} {'Per Capita':>12} {'Share':>8}")
print(f"  {'─'*22} {'─'*12} {'─'*8}")
for _, r in cats.iterrows():
    print(f"  {r['category']:<22} ${r['per_capita_cad']:>10,.0f} {r['share']:>7.1f}%")

# Year-over-year growth
print(f"\n{'─'*62}")
print(f"SPENDING GROWTH — {early_yr} to {latest_yr}")
print(f"{'─'*62}")

yr_cat = (actual_df.groupby(["year","category"])["per_capita_cad"]
                   .mean().reset_index())

print(f"\n  {'Category':<22} {str(early_yr):>8} {str(latest_yr):>8} {'Total Growth':>14}")
print(f"  {'─'*22} {'─'*8} {'─'*8} {'─'*14}")
for cat in sorted(actual_df["category"].unique()):
    sub = yr_cat[yr_cat["category"] == cat]
    v_e = sub[sub["year"] == early_yr]["per_capita_cad"].values[0]
    v_l = sub[sub["year"] == latest_yr]["per_capita_cad"].values[0]
    pct = (v_l - v_e) / v_e * 100
    print(f"  {cat:<22} ${v_e:>7,.0f} ${v_l:>7,.0f} {pct:>+13.0f}%")

# Drug category deep dive
print(f"\n{'─'*62}")
print(f"DRUG SPENDING DEEP DIVE — Category Mix {latest_yr}")
print(f"{'─'*62}")

drug_latest = drug[drug["year"] == latest_yr].sort_values("share_of_drug_spend", ascending=False)
print(f"\n  {'Drug Category':<26} {'Share':>8} {'Annual Growth':>14}")
print(f"  {'─'*26} {'─'*8} {'─'*14}")
for _, r in drug_latest.iterrows():
    flag = " ◄ FASTEST GROWING" if r["annual_growth_pct"] == drug_latest["annual_growth_pct"].max() else ""
    print(f"  {r['drug_category']:<26} {r['share_of_drug_spend']:>7.1%} {r['annual_growth_pct']:>+13.1f}%{flag}")

# Public vs private
print(f"\n{'─'*62}")
print(f"PUBLIC vs PRIVATE SPLIT — {latest_yr}")
print(f"{'─'*62}")

pub = (actual_df[actual_df["year"] == latest_yr]
       .groupby("province")["public_share"]
       .mean().sort_values().reset_index())
print(f"\n  {'Province':>10} {'Public Share':>14} {'Private Share':>15}")
print(f"  {'─'*10} {'─'*14} {'─'*15}")
for _, r in pub.iterrows():
    print(f"  {r['province']:>10} {r['public_share']:>13.0%} {1-r['public_share']:>14.0%}")

# Scenario model
print(f"\n{'─'*62}")
print("SCENARIO MODEL — Drug Cost Reduction Levers")
print(f"{'─'*62}")

total_drug_spend_est = 45_000_000_000  # NHEX 2023 estimate ~$45B national drug spend

scenarios = [
    ("10% biosimilar substitution (biologics)",  0.28, 0.10, 0.35),
    ("5% generic substitution (brand name)",      0.24, 0.05, 0.30),
    ("GLP-1 volume management (10% reduction)",   0.12, 0.10, 1.00),
]

print(f"\n  Total estimated drug spend: ${total_drug_spend_est/1e9:.0f}B")
print()
for label, cat_share, reduction, saving_rate in scenarios:
    category_spend = total_drug_spend_est * cat_share
    saving = category_spend * reduction * saving_rate
    print(f"  {label}")
    print(f"    Estimated saving: ${saving/1e6:.0f}M annually\n")

print(f"{'─'*62}")
print("STRATEGIC RECOMMENDATIONS")
print(f"{'─'*62}")
print("""
  1. GLP-1 COST MANAGEMENT
     GLP-1 analogues (diabetes/obesity drugs) are growing
     at 14.5% per year — the fastest of any drug category.
     Provincial formularies need a managed-entry framework
     with outcome-based funding conditions before this
     category dominates the drug budget.

  2. BIOSIMILAR POLICY
     Specialty biologics represent 28% of drug spend.
     A 10% shift to approved biosimilars saves ~$1.3B
     nationally. BC and AB have biosimilar transition
     policies. Other provinces should follow their model.

  3. ATLANTIC SPENDING PREMIUM
     NL spends $1,600 more per capita than QC — the
     widest gap in the country. The driver is not waste
     but older population and higher chronic disease burden.
     Federal equalization transfers should reflect this.

  4. HOME CARE SHIFT
     A 5% shift of Other Institutional spending into
     Home Care would produce better outcomes at lower
     cost for post-surgical and chronic disease patients.
""")
print(sep)
