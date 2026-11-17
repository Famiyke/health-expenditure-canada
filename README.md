# Project 3: Canadian Health Expenditure Analysis

> **DATA PROVENANCE:** This portfolio project uses simulated records informed by named Canadian public sources. All generated statistics, rankings, demographic differences, and savings models are illustrative rather than verified official estimates. Recommendations are hypothetical scenarios, not observed effects.

**Domain:** Health Finance
**Tools:** Python · Excel · SQL
**Public reference source (distinct from simulated analysis data):** CIHI National Health Expenditure Trends (NHEX) 2025
**Download:** https://www.cihi.ca/en/national-health-expenditure-trends → "Data Tables" → Download Excel (free, no registration)

---

## Business Question
How is health spending distributed across provinces and categories, what is driving drug cost growth, and where are the highest-value opportunities to slow spending without reducing outcomes?

---

## How to Get the Real Data
1. Go to: https://www.cihi.ca/en/national-health-expenditure-trends
2. Click **NHEX trends data** → **Download data tables**
3. Download Series A (national totals and use of funds)
4. Rename file: `nhex-series-a-2025-en.xlsx`
5. Place in this folder — `analysis.py` reads it directly

## How to Run (demo mode)
```bash
pip install pandas numpy openpyxl
python simulate_nhex_data.py   # creates nhex_combined.csv and nhex_drug_detail.csv
python analysis.py             # full analysis — cleaning, spending trends, drug deep dive
```

---

## Analyst Roles

| Hat | What I Did |
|-----|-----------|
| Data Detective | Loaded multi-tab NHEX Excel files, standardised province labels, separated actual vs forecast year flags, validated per-capita ranges |
| SQL/Python Programmer | Analysed per-capita spending by province, category growth rates, drug sub-category mix, public vs private splits, scenario modelling |
| Dashboard Architect | Built Excel workbook with 6 sheets: Dashboard (4 charts), Summary (KPIs and findings), Total Spending, Spending by Category, Public vs Private, Drug Spending |
| Data Storyteller | Wrote a CFO-ready expenditure brief for a provincial health finance committee |
| Strategic Consultant | Identified three drug spending levers: GLP-1 management, biosimilar substitution, and home care shift |

---

## Illustrative Findings From Generated Data

1. **Physician services grew the fastest of any spending category.** Up 65% between 2015 and 2023 — well above hospitals (+50%), drugs (+35%), and public health (+36%). This reflects fee schedule increases and an expanded scope of funded services, not just volume growth.

2. **NL spends $1,711 more per capita than QC — the widest provincial gap.** NL ($10,267) and AB ($9,881) are the highest spenders. QC ($8,556) is the most efficient. The Atlantic spending premium reflects older populations and higher chronic disease burden, not administrative waste.

3. **GLP-1 analogues are the fastest-growing drug sub-category at 14.5% annually.** These diabetes and obesity medications are growing nearly 5x faster than generic drugs. Without a managed-entry framework, this category will disproportionately consume provincial drug budgets within 5 years.

4. **Hospitals still dominate the budget at 26.3% of total spending.** Despite two decades of health system reform, the hospital share has not meaningfully declined. A 5% shift from Other Institutional care ($914 per capita) to home care would reduce costs while improving outcomes for post-surgical and chronic disease patients.

---

## Excel Workbook

**File:** `nhex_excel_workbook.xlsx` — built using real CIHI NHEX 2025 data

| Sheet | Contents |
|-------|---------|
| Dashboard | 4 charts: total spending trend, category comparison, public vs private stacked bar, drug vs hospital trend |
| Summary | KPI cards and 6 key findings |
| Total Spending | Annual total, per capita, GDP share, YOY growth — 2000–2023 |
| Spending by Category | 9 categories by year with budget share row |
| Public vs Private | Public/private split by year with average row |
| Drug Spending | Drug vs hospital spending trend with YOY growth |

---

## Hypothetical Recommendations

1. **GLP-1 cost management.** GLP-1 analogues are growing at 14.5% per year. Provincial formularies need outcome-based funding conditions and volume management before this category dominates the drug budget.

2. **Biosimilar substitution policy.** Specialty biologics represent 27.8% of drug spend. A 10% shift to approved biosimilars saves an estimated $438M nationally. BC and AB already have biosimilar transition policies — other provinces should follow.

3. **Atlantic spending equity.** NL spends $1,711 more per capita than QC. The driver is population demographics and chronic disease burden, not inefficiency. Federal equalization transfers should reflect this structural gap.

4. **Home care shift.** A 5% reallocation from Other Institutional spending to home care would produce better outcomes at lower cost for post-surgical and chronic disease patients. Home care currently receives only 3–4% of the total health budget.

---

## Files

| File | Purpose |
|------|---------|
| `simulate_nhex_data.py` | Builds representative dataset from published CIHI NHEX provincial and category figures |
| `analysis.py` | Data profiling, per-capita ranking, category growth, drug deep dive, scenario modelling, recommendations |
| `sql_queries.sql` | 8 SQL queries covering spending by province, category, drug mix, and public/private split |
| `nhex_excel_workbook.xlsx` | Full Excel workbook with Dashboard, data sheets, and charts — real CIHI NHEX 2025 data |
| `expenditure_brief.md` | CFO-ready findings brief for a provincial health finance committee |

---

## Data Provenance and Limitations

The Excel workbook is described as using an actual CIHI NHEX source workbook; the Python analysis is simulated. Do not present the simulated category growth rates, interprovincial spending differences, GLP-1 trends, or biosimilar savings as measured CIHI findings. Confirm fiscal/calendar year, actual/projected amounts, price basis, geography, and denominators against original tables.

This project uses the real CIHI NHEX 2025 Series A Excel file as its primary data source for the Excel workbook. The Python analysis uses a simulation anchored to the same published CIHI figures. All source statistics are documented in `simulate_nhex_data.py`.
