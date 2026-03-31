# Project 3 — Excel Workbook Guide
## Canadian Health Expenditure Tracker

**File to create:** `NHEX_Expenditure_Tracker.xlsx`  
**Source data:** `nhex_combined.csv` and `nhex_drug_detail.csv`

---

## Tab 1: Raw Data

1. Data → From Text/CSV → select `nhex_combined.csv` → Load
2. Rename sheet: `Spending_Data`
3. Format `per_capita_cad` as Currency (CAD, 0 decimals)
4. Format `public_share` as Percentage (1 decimal)
5. Add a helper column `Decade`:
   ```
   =IF(A2<2020,"2015-2019","2020-2024")
   ```
6. Add a helper column `Forecast_Flag`:
   ```
   =IF(G2=TRUE,"Forecast","Actual")
   ```
7. Convert to Table (Ctrl+T) → name it `SpendingData`

---

## Tab 2: Province Summary (PivotTable)

1. Insert → PivotTable → from `SpendingData` → New Sheet
2. Rename: `Province_Summary`
3. Setup:
   - **Rows:** `province`
   - **Columns:** `year`
   - **Values:** Sum of `per_capita_cad`
   - **Filter:** `is_forecast` = FALSE (actual only)
4. Add a Total column using:
   ```
   =AVERAGE(B2:K2)
   ```
   Label: "Avg Per Capita"
5. Conditional formatting on all value cells:
   - Color scale: white (low) → dark blue (high)
6. Insert → PivotChart → Line chart showing per-capita trend by province

---

## Tab 3: Category Breakdown (PivotTable)

1. New PivotTable → rename: `Category_Mix`
2. Setup:
   - **Rows:** `category`
   - **Values:** Sum of `per_capita_cad` (filtered to latest actual year)
3. Add a helper column for % of total:
   ```
   =B2/SUM($B$2:$B$10)
   ```
4. Insert → PivotChart → Donut chart (category share)
5. Add a second chart → Bar chart showing growth by category year over year

---

## Tab 4: Drug Deep Dive (from nhex_drug_detail.csv)

1. Load `nhex_drug_detail.csv` as second table → rename: `Drug_Data`
2. New PivotTable from Drug_Data → rename sheet: `Drug_Analysis`
3. Setup:
   - **Rows:** `drug_category`
   - **Columns:** `year`
   - **Values:** Average of `share_of_drug_spend`
4. Conditional formatting: highlight highest-growth row (GLP-1) in orange
5. Insert a line chart: GLP-1 share trend vs. all other categories
6. Add text box annotation: "GLP-1 fastest growing at 14.5%/yr"

---

## Tab 5: Scenario Model

Create manually (no pivot needed):

**Row headers:**

| Label | Formula |
|-------|---------|
| Total Drug Spend ($B) | =45 (NHEX 2023 estimate) |
| Biologics Share (%) | =28% |
| Generic Share (%) | =24% |
| GLP-1 Share (%) | =12% |

**Scenario inputs (yellow cells — user adjustable):**

| Input | Default |
|-------|---------|
| Biosimilar substitution rate | 10% |
| Generic substitution rate | 5% |
| GLP-1 volume reduction | 10% |
| Biosimilar price discount | 35% |

**Scenario outputs:**

```excel
Biologic saving   = B2 * 1e9 * B4 * B8 * B12 / 1e6
Generic saving    = B2 * 1e9 * B5 * B9 * 0.30 / 1e6
GLP-1 saving      = B2 * 1e9 * B6 * B10 * 1.00 / 1e6
Total saving      = SUM(biologic, generic, GLP-1)
```

Format outputs in green cells with `$#,##0"M"` format.

Add a bar chart showing savings by lever.

---

## Tab 6: Dashboard

1. Insert blank sheet → rename: `Dashboard`
2. Set tab colour to dark blue

**Section A: Header KPIs (linked cells)**
- National Avg Per Capita: link to Province_Summary calculated field
- Highest Spending Province: use `=INDEX()` + `MATCH()` on Province_Summary
- Drug Spend Growth: link from Category_Mix

**Section B: Copy charts from Tabs 2, 3, 4 as linked images**
(Right-click chart → Copy → Paste Special → Linked Picture)

**Section C: Scenario summary box**
Link to key outputs from Tab 5

**Formatting:**
- Dark navy header row: `#1A2744`
- White text in headers
- Light grey section backgrounds: `#F4F4F4`
- All KPI numbers: 20pt bold, accent blue
