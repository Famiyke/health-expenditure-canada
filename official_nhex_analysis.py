"""Analyse the official CIHI 2026 NHEX Series A extraction, not simulated data.

Inputs: official_nhex_2026_national.csv from official_nhex_2026.py.
Outputs: source-traceable descriptive growth table and Markdown analysis.
All amounts use current-price Canadian dollars unless labelled otherwise.
2025/2026 forecasts must not be described as observed spending.
"""
import csv
from pathlib import Path

INPUT = Path("official_nhex_2026_national.csv")
DETAIL = Path("official_nhex_2026_annual_growth.csv")
REPORT = Path("OFFICIAL_NHEX_2026_FINDINGS.md")


def main():
    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 52
    assert [int(r["year"]) for r in rows] == list(range(1975, 2027))
    assert [int(r["year"]) for r in rows if r["release_status"] == "forecast"] == [2025, 2026]

    growth_rows = []
    by_year = {}
    for i, r in enumerate(rows):
        year = int(r["year"])
        value = float(r["total_current_cad_billions"])
        prev = float(rows[i - 1]["total_current_cad_billions"]) if i else None
        growth = (value / prev - 1) * 100 if prev else None
        by_year[year] = r
        growth_rows.append({
            "year": year,
            "status": r["release_status"],
            "current_cad_billions": f"{value:.6f}",
            "year_over_year_percent": f"{growth:.4f}" if growth is not None else "",
            "growth_interpretation": "forecast comparison" if r["release_status"] == "forecast" else "historical change",
            "source_sheet": r["source_sheet"],
            "source_row": r["source_row"],
            "source_url": r["source_url"]
        })

    with DETAIL.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(growth_rows[0]))
        writer.writeheader()
        writer.writerows(growth_rows)

    a = lambda y: float(by_year[y]["total_current_cad_billions"])
    c = lambda y: float(by_year[y]["per_capita_current_cad"])
    g = lambda y: float(by_year[y]["health_expenditure_share_gdp_percent"])
    yoy_2024 = (a(2024) / a(2023) - 1) * 100
    change_2019_24 = (a(2024) / a(2019) - 1) * 100
    text = f"""# Canada's health expenditure, 1975–2026 | CIHI actual data and forecasts

**Dataset:** Official CIHI NHEX 2026, Series A, worksheet **Summary**, Table **A.1.a**. This analysis uses downloaded official CIHI aggregate numbers, **not simulated records**.

**Source:** https://www.cihi.ca/sites/default/files/document/nhex-series-a-2026-en.xlsx

## Confirmed official measurements

| Indicator | Value | Source |
|---|---:|---|
| 2023 total health expenditure, current CAD | ${a(2023):,.2f} billion | Summary!B52 |
| 2024 total health expenditure, current CAD | ${a(2024):,.2f} billion | Summary!B53 |
| 2024 health spending per capita | ${c(2024):,.0f} | Summary!C53 |
| 2024 health spending as share of GDP | {g(2024):.2f}% | Summary!F53 |
| Observed 2024 growth in nominal total spending | {yoy_2024:.2f}% | Derived from Summary!B52:B53 |
| Nominal spending change, 2019 to 2024 | {change_2019_24:.2f}% | Derived from Summary!B48 and B53 |

## CIHI forecast figures, NOT observed actual expenditures

| Forecast year | Projected total, current CAD | Source |
|---|---:|---|
| 2025 | ${a(2025):,.2f} billion | Summary!B54 |
| 2026 | ${a(2026):,.2f} billion | Summary!B55 |

## Definition and quality controls

- **Actual/revised years:** 1975–2024 in this release. CIHI revises historical values across publication editions.
- **Forecast years:** 2025 and 2026 are marked 'f' in CIHI's source worksheet.
- **Nominal dollars:** Current-price spending is not adjusted for inflation. Changes reflect both price and volume effects.
- **Constant dollars:** The extract also contains CIHI's 2010-dollar constant-price spending. It should not be mixed with current dollars in the same growth series.
- **Population:** Per-capita values come directly from CIHI and are not calculated using an external population series.
- **Interpretation:** These aggregate totals do not establish causes, program outcomes, waste, avoidable spending, or healthcare quality. They are not suitable for hospital/provider comparisons.
- **Reproducibility:** Re-run `python official_nhex_2026.py` and `python official_nhex_analysis.py`. Every extracted annual record retains the original CIHI worksheet row and source URL.

This project replaces unsupported simulated national-spending claims with **real CIHI observations and explicit forecasts**. A separate synthetic scenario project remains archived for methodological demonstration.
"""
    REPORT.write_text(text, encoding="utf-8")
    assert a(2024) > a(2023) and a(2026) > a(2025)
    assert by_year[2025]["release_status"] == "forecast"
    print(f"Verified official CIHI 2024 spending: ${a(2024):,.2f}B")
    print(f"Nominal 2024 growth: {yoy_2024:.2f}%")
    print(f"Created {DETAIL} and {REPORT}")


if __name__ == "__main__":
    main()
