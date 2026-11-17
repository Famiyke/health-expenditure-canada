# Health Expenditure Analysis | Illustrative Finance Brief

> **Data-source boundary:** The Excel workbook is described as using CIHI NHEX source tables. The Python expenditure and drug-detail analysis uses simulated data. Do not interpret its modeled outputs as CIHI estimates.

## Decision question
How can a healthcare finance team compare spending categories and assess hypothetical budget changes?

## Analytical deliverables
- An Excel workbook described in the repository as based on CIHI NHEX tables.
- Python and SQL examples using separately generated data.
- Scenario calculations that illustrate the effect of alternative assumptions.

## Interpretation
Numerical growth rates and projections from the simulated Python analysis are not official drug-market forecasts. Potential biosimilar, home care or other savings are hypothetical and exclude implementation costs and uncertainty.

## Verification required before decisions
1. Reconcile the Excel workbook directly to CIHI NHEX tables.
2. Specify reporting years, expenditure definitions, projection status and price basis.
3. Calculate category shares with consistent denominators.
4. Document drug-class source data and ranges for scenario assumptions.
5. Avoid inferring causes of provincial differences without supporting analysis.

## Supporting material
See [Excel workbook](nhex_excel_workbook.xlsx), [Python analysis](analysis.py) and [README](README.md).
