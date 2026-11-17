# Independently reproduced NHEX comparison: portfolio workbook vs CIHI 2026

**Completed:** 17 November 2026

## Sources and method

The original portfolio workbook `nhex_excel_workbook.xlsx` contains an expenditure series labelled as CIHI NHEX 2025, covering 2000–2023. I downloaded the official **CIHI National Health Expenditure Trends 2026, Series A** Excel workbook from:

https://www.cihi.ca/sites/default/files/document/nhex-series-a-2026-en.xlsx

For each year, I compared the portfolio `Total Spending` worksheet (year, total spending in $ billions, per capita, spending as share of GDP) against official Series A `Summary`, Table A.1.a (millions of dollars converted to billions; GDP percent converted to percentage points). A companion CSV records **all 24 matched years**:

[Download the 24-year reconciliation table](reconciliation_nhex_2026_vs_portfolio_2000_2023.csv)

**Caution:** This is a cross-release comparison of an older portfolio series with the updated 2026 release. Differences do **not** automatically establish errors, because CIHI updates historical estimates and the portfolio rounds values.

## Results: 2000–2023

- Matched years: **24 of 24**.
- Mean absolute difference in total expenditure: **approximately $0.13 billion per year**.
- Mean absolute difference in per-capita expenditure: **approximately $4 per person**.
- Mean absolute difference in share of GDP: **approximately 0.03 percentage points**.
- Largest total spending difference: **2023**; portfolio **$360.70B**, CIHI 2026 **$362.183B**, portfolio minus current release **−$1.483B**.
- The portfolio's total spending line and category sum are internally consistent to within **$0.05B** in every reported year, which is consistent with rounding.

## 2023 category checks, $ billions

| Category | Portfolio | CIHI 2026 Series A | Portfolio minus 2026 |
|---|---:|---:|---:|
| Hospitals | 94.47 | 94.38 | +0.09 |
| Other institutions | 47.41 | 47.43 | −0.02 |
| Physicians | 48.02 | 48.02 | approximately 0.00 |
| Other professionals | 38.91 | 38.73 | +0.18 |
| Total drugs | 49.03 | 48.84 | +0.19 |
| Public health | 21.37 | 23.29 | **−1.92** |
| Administration | 11.97 | 12.08 | −0.11 |
| Other health | 33.83 | 33.76 | +0.07 |
| Capital | 15.65 | 15.65 | approximately 0.00 |

These values compare different CIHI release vintages. The notably larger 2023 public-health difference **requires source-vintage and classification reconciliation**, not an automatic overwrite of the earlier workbook's value.

## Interpretation

This establishes that the portfolio's 2000–2023 national total expenditure trajectory is broadly close to an official, more recent CIHI series, while retaining source-year and revision differences.

It does **not** independently verify all categories, source finance figures, drug projections, hypothetical savings, provincial data, the simulated Python dataset, or the Excel workbook's complete source lineage.

**Next release requirement:** Obtain the exact 2025 CIHI Series A workbook and reconcile each category and the 2023 public-health figure by edition, unit, classification, and source cell before claiming an exact reproduction of CIHI NHEX 2025.

