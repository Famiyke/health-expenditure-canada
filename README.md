# Project 3: Canadian Health Expenditure Analysis

**Domain:** Health Finance / Insurance  
**Tools:** Python · Excel · Power BI  
**Real Data Source:** CIHI National Health Expenditure Trends (NHEX)  
**Download:** https://www.cihi.ca/en/national-health-expenditure-trends → "Data Tables" → Download Excel (free, no registration)

---

## Business Question
How is health spending distributed across provinces and categories, what is driving drug cost growth, and where are the highest-value opportunities to slow spending without reducing outcomes?

---

## How to Get the Real Data
1. Go to: https://www.cihi.ca/en/national-health-expenditure-trends
2. Click **NHEX trends data** → **Download data tables**
3. Download Series B (provincial) and Series C (use of funds / drug spending)
4. Rename files: `nhex_series_b.xlsx` and `nhex_series_c.xlsx`
5. Place in this folder — `01_load_clean.py` auto-detects them

## How to Run (demo mode)
```bash
pip install pandas numpy openpyxl
python simulate_nhex_data.py   # creates nhex_combined.csv
python 01_clean_explore.py     # data detective
python 02_analysis.py          # full analysis
```

---

## Analyst Roles

| Hat | What I Did |
|-----|-----------|
| Data Detective | Loaded multi-tab Excel NHEX files, standardised province labels, handled forecast vs. actual year flags |
| SQL/Python Programmer | Analysed per-capita spending, drug cost growth, public vs. private split |
| Dashboard Architect | Built Excel workbook with pivot tables + charts + scenario model |
| Data Storyteller | Wrote a CFO-ready expenditure brief |
| Strategic Consultant | Identified three spending levers: biosimilars, generic substitution, and home care shift |

---

## Files

| File | Purpose |
|------|---------|
| `simulate_nhex_data.py` | Builds representative dataset from published NHEX figures |
| `01_load_clean.py` | Load Excel, standardise, flag forecast years |
| `02_analysis.py` | Spending trends, drug analysis, provincial gaps |
| `nhex_excel_workbook.xlsx` | Full Excel workbook — Dashboard, data sheets, charts. Real CIHI NHEX 2025 data. |
| `expenditure_brief.md` | CFO-ready findings brief |
