"""Extract ACTUAL CIHI national health expenditure observations from Series A.

Source: CIHI NHEX trends 2026, Series A, Summary / Table A.1.a.
https://www.cihi.ca/sites/default/files/document/nhex-series-a-2026-en.xlsx

This script does not read or use simulate_nhex_data.py. The original CIHI
source is fetched each run. Years marked "f" are forecasts, not actuals.
All expenditure amounts are nominal/current CAD, not inflation-adjusted.
"""
import csv
import io
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from zipfile import ZipFile

SOURCE_URL = "https://www.cihi.ca/sites/default/files/document/nhex-series-a-2026-en.xlsx"
OUTPUT = pathlib.Path("official_nhex_2026_national.csv")
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def extract_records(data: bytes):
    """Read only observed Series A Summary, A.1.a cells A:F."""
    with ZipFile(io.BytesIO(data)) as archive:
        strings_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        strings = [
            "".join((t.text or "") for t in si.iter(M + "t"))
            for si in strings_root.findall(M + "si")
        ]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet3.xml"))
        rows = []
        for row in sheet.findall(".//" + M + "sheetData/" + M + "row"):
            rownum = int(row.get("r", "-1"))
            if rownum < 4 or rownum > 55:
                continue
            cells = {}
            for cell in row.findall(M + "c"):
                ref = cell.get("r", "")
                col = re.match(r"^[A-Z]+", ref)
                if not col or col.group() not in "ABCDEF":
                    continue
                v = cell.find(M + "v")
                if v is None or v.text is None:
                    continue
                val = strings[int(v.text)] if cell.get("t") == "s" else v.text
                cells[col.group()] = val
            year_label = cells.get("A", "").strip()
            match = re.fullmatch(r"(19\d\d|20\d\d)(?:\s*f)?", year_label)
            if not match:
                raise ValueError(f"Unexpected CIHI year label in row {rownum}: {year_label!r}")
            forecast = year_label.endswith("f")
            if not all(k in cells for k in "ABCDEF"):
                raise ValueError(f"Missing source field in row {rownum}")
            values = [float(cells[k]) for k in "BCDEF"]
            rows.append({
                "year": int(match.group(1)),
                "release_status": "forecast" if forecast else "actual_or_revised",
                "total_current_cad_billions": round(values[0] / 1000, 6),
                "per_capita_current_cad": round(values[1], 4),
                "total_2010_constant_cad_billions": round(values[2] / 1000, 6),
                "per_capita_2010_constant_cad": round(values[3], 4),
                "health_expenditure_share_gdp_percent": round(values[4], 4),
                "source_sheet": "Summary",
                "source_table": "A.1.a",
                "source_row": rownum,
                "source_release": "CIHI NHEX 2026 Series A",
                "source_url": SOURCE_URL,
            })
    years = [r["year"] for r in rows]
    assert len(rows) == 52 and years == list(range(1975, 2027)), years
    assert [r["year"] for r in rows if r["release_status"] == "forecast"] == [2025, 2026]
    assert 362 < next(r["total_current_cad_billions"] for r in rows if r["year"] == 2023) < 363
    return rows


def main():
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=50) as response:
        raw = response.read()
    if not raw.startswith(b"PK"):
        raise ValueError("CIHI response was not an Excel archive")
    records = extract_records(raw)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} real CIHI Series A records to {OUTPUT}")
    for year in (2023, 2024, 2025, 2026):
        row = next(r for r in records if r["year"] == year)
        print(year, row["release_status"], row["total_current_cad_billions"],
              "billions CAD", row["source_sheet"] + "!" + "B" + str(row["source_row"]))


if __name__ == "__main__":
    main()
