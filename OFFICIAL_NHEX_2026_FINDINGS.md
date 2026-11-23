# Canada's health expenditure, 1975–2026 | CIHI actual data and forecasts

**Dataset:** Official CIHI NHEX 2026, Series A, worksheet **Summary**, Table **A.1.a**. The annual figures come directly from the published CIHI worksheet.

**Source:** https://www.cihi.ca/sites/default/files/document/nhex-series-a-2026-en.xlsx

## Historical figures

| Indicator | Value | Source |
|---|---:|---|
| 2023 total health expenditure, current CAD | $362.18 billion | Summary!B52 |
| 2024 total health expenditure, current CAD | $392.82 billion | Summary!B53 |
| 2024 health spending per capita | $9,520 | Summary!C53 |
| 2024 health spending as share of GDP | 12.64% | Summary!F53 |
| Observed 2024 growth in nominal total spending | 8.46% | Derived from Summary!B52:B53 |
| Nominal spending change, 2019 to 2024 | 45.60% | Derived from Summary!B48 and B53 |

## CIHI forecasts

| Forecast year | Projected total, current CAD | Source |
|---|---:|---|
| 2025 | $413.11 billion | Summary!B54 |
| 2026 | $433.12 billion | Summary!B55 |

## Definition and quality controls

- **Actual/revised years:** 1975–2024 in this release. CIHI revises historical values across publication editions.
- **Forecast years:** 2025 and 2026 are marked 'f' in CIHI's source worksheet.
- **Nominal dollars:** Current-price spending is not adjusted for inflation. Changes reflect both price and volume effects.
- **Constant dollars:** The extract also contains CIHI's 2010-dollar constant-price spending. It should not be mixed with current dollars in the same growth series.
- **Population:** Per-capita values come directly from CIHI and are not calculated using an external population series.
- **Interpretation:** These aggregate totals do not establish causes, program outcomes, waste, avoidable spending, or healthcare quality. They are not suitable for hospital/provider comparisons.
- **Reproducibility:** Re-run `python official_nhex_2026.py` and `python official_nhex_analysis.py`. Every extracted annual record retains the original CIHI worksheet row and source URL.

The earlier simulated workbook remains available as a separate educational scenario.
