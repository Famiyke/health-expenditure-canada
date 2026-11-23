"""Read CIHI's National Health Expenditure Trends 2026, Summary Table A.1.a.

The worksheet includes current-price spending, spending in constant 2010 dollars,
per-capita amounts and health spending as a share of GDP. CIHI marks forecasts
with an "f". The output preserves those labels and the original worksheet rows.
"""

import argparse
import csv
import io
import re
from pathlib import Path
from urllib.request import Request, urlopen

from openpyxl import load_workbook

SOURCE_URL = "https://www.cihi.ca/sites/default/files/document/nhex-series-a-2026-en.xlsx"
OUTPUT = Path("official_nhex_2026_national.csv")


def extract_records(data: bytes):
    """Read the six published columns of the Summary worksheet."""
    workbook = load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    try:
        sheet = workbook["Summary"]
        records = []
        for source_row, cells in enumerate(
            sheet.iter_rows(min_row=4, max_row=55, max_col=6, values_only=True), start=4
        ):
            year, current_total, current_per_capita, constant_total, constant_per_capita, gdp = (
                cells
            )
            year_label = str(year).strip()
            match = re.fullmatch(r"(19\d\d|20\d\d)(?:\s*f)?", year_label)
            if not match:
                raise ValueError(f"Unexpected CIHI year label in row {source_row}: {year_label!r}")
            if any(value is None for value in cells):
                raise ValueError(f"Missing source field in row {source_row}")
            records.append(
                {
                    "year": int(match.group(1)),
                    "release_status": (
                        "forecast" if year_label.endswith("f") else "actual_or_revised"
                    ),
                    # CIHI's total-spending columns are in millions; report billions.
                    "total_current_cad_billions": round(float(current_total) / 1000, 6),
                    "per_capita_current_cad": round(float(current_per_capita), 4),
                    "total_2010_constant_cad_billions": round(float(constant_total) / 1000, 6),
                    "per_capita_2010_constant_cad": round(float(constant_per_capita), 4),
                    "health_expenditure_share_gdp_percent": round(float(gdp), 4),
                    "source_sheet": "Summary",
                    "source_table": "A.1.a",
                    "source_row": source_row,
                    "source_release": "CIHI NHEX 2026 Series A",
                    "source_url": SOURCE_URL,
                }
            )
    finally:
        workbook.close()

    # These checks apply to the November 2026 release.
    assert [row["year"] for row in records] == list(range(1975, 2027))
    assert [row["year"] for row in records if row["release_status"] == "forecast"] == [2025, 2026]
    assert (
        362
        < next(row["total_current_cad_billions"] for row in records if row["year"] == 2023)
        < 363
    )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Use an already downloaded CIHI workbook")
    args = parser.parse_args()
    if args.source:
        data = args.source.read_bytes()
    else:
        request = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=50) as response:
            data = response.read()
    if not data.startswith(b"PK"):
        raise ValueError("The source file is not an Excel workbook")
    records = extract_records(data)
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} annual CIHI observations and forecasts to {OUTPUT}")
    for year in (2023, 2024, 2025, 2026):
        row = next(record for record in records if record["year"] == year)
        print(
            year,
            row["release_status"],
            row["total_current_cad_billions"],
            "billions CAD",
            f"Summary!B{row['source_row']}",
        )


if __name__ == "__main__":
    main()
