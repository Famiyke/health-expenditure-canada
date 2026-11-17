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

## Illustrative analytical outputs

This project's Python/SQL outputs illustrate data processing, comparisons, modeling and reporting using generated records. The specific rates, rankings, cost figures and trends in the demonstration are **not verified official findings**. See the analysis scripts for the computations and the data limitations section below for interpretation requirements.

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

## Interpretation and real-world next steps

Use the simulated findings to demonstrate analytical methods, not to rank actual jurisdictions or recommend clinical or policy interventions. A real decision requires matched official data, documented definitions, relevant uncertainty, and clinical or operational stakeholder review. Financial scenarios must include assumptions, costs and sensitivity analysis.

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
