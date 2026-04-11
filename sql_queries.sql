-- Project 3: Canadian Health Expenditure Analysis
-- sql_queries.sql — SQL Programmer Hat
-- Load nhex_combined.csv as table: nhex
-- Load nhex_drug_detail.csv as table: drug
-- Works in DB Browser for SQLite, DBeaver, or any SQL tool

-- ── 1. Per-capita total spending by province — latest actual year ──────────────
SELECT
    province,
    ROUND(SUM(per_capita_cad), 0)                   AS total_per_capita,
    ROUND(SUM(per_capita_cad)
          - AVG(SUM(per_capita_cad)) OVER (), 0)    AS vs_national_avg
FROM nhex
WHERE year = (SELECT MAX(year) FROM nhex WHERE is_forecast = 0)
  AND is_forecast = 0
GROUP BY province
ORDER BY total_per_capita DESC;

-- ── 2. Spending by category — latest year share of total ──────────────────────
SELECT
    category,
    ROUND(AVG(per_capita_cad), 0)                   AS avg_per_capita,
    ROUND(AVG(per_capita_cad)
          / SUM(AVG(per_capita_cad)) OVER () * 100, 1) AS share_of_total_pct
FROM nhex
WHERE year = (SELECT MAX(year) FROM nhex WHERE is_forecast = 0)
  AND is_forecast = 0
GROUP BY category
ORDER BY avg_per_capita DESC;

-- ── 3. Year-over-year growth by category ──────────────────────────────────────
SELECT
    category,
    ROUND(AVG(CASE WHEN year = (SELECT MIN(year) FROM nhex WHERE is_forecast = 0)
                   THEN per_capita_cad END), 0)     AS earliest_per_capita,
    ROUND(AVG(CASE WHEN year = (SELECT MAX(year) FROM nhex WHERE is_forecast = 0)
                   THEN per_capita_cad END), 0)     AS latest_per_capita,
    ROUND(
        (AVG(CASE WHEN year = (SELECT MAX(year) FROM nhex WHERE is_forecast = 0)
                  THEN per_capita_cad END)
       - AVG(CASE WHEN year = (SELECT MIN(year) FROM nhex WHERE is_forecast = 0)
                  THEN per_capita_cad END))
       / AVG(CASE WHEN year = (SELECT MIN(year) FROM nhex WHERE is_forecast = 0)
                  THEN per_capita_cad END) * 100
    , 1)                                            AS pct_growth
FROM nhex
WHERE is_forecast = 0
GROUP BY category
ORDER BY pct_growth DESC;

-- ── 4. Public vs private split by province ────────────────────────────────────
SELECT
    province,
    ROUND(AVG(public_share) * 100, 1)              AS avg_public_pct,
    ROUND((1 - AVG(public_share)) * 100, 1)        AS avg_private_pct
FROM nhex
WHERE year = (SELECT MAX(year) FROM nhex WHERE is_forecast = 0)
  AND is_forecast = 0
GROUP BY province
ORDER BY avg_public_pct ASC;  -- lowest public share first

-- ── 5. Trend — total per-capita spending all provinces by year ─────────────────
SELECT
    year,
    ROUND(AVG(SUM(per_capita_cad)) OVER
          (PARTITION BY year), 0)                  AS national_avg_per_capita,
    MIN(SUM(per_capita_cad))                        AS lowest_province,
    MAX(SUM(per_capita_cad))                        AS highest_province,
    MAX(SUM(per_capita_cad))
    - MIN(SUM(per_capita_cad))                      AS provincial_spread
FROM nhex
WHERE is_forecast = 0
GROUP BY year, province
ORDER BY year;

-- ── 6. Drug category mix and growth ───────────────────────────────────────────
SELECT
    drug_category,
    ROUND(AVG(share_of_drug_spend) * 100, 1)       AS avg_share_pct,
    ROUND(AVG(annual_growth_pct), 1)               AS annual_growth_pct
FROM drug
WHERE year = (SELECT MAX(year) FROM drug)
GROUP BY drug_category
ORDER BY annual_growth_pct DESC;

-- ── 7. Hospital vs drug spending gap over time ────────────────────────────────
SELECT
    year,
    ROUND(AVG(CASE WHEN category = 'Hospitals'
                   THEN per_capita_cad END), 0)    AS hospital_per_capita,
    ROUND(AVG(CASE WHEN category = 'Drugs'
                   THEN per_capita_cad END), 0)    AS drug_per_capita,
    ROUND(
        AVG(CASE WHEN category = 'Drugs' THEN per_capita_cad END)
      / AVG(CASE WHEN category = 'Hospitals' THEN per_capita_cad END) * 100
    , 1)                                           AS drug_as_pct_of_hospital
FROM nhex
WHERE is_forecast = 0
GROUP BY year
ORDER BY year;

-- ── 8. Provinces above and below national average — latest year ───────────────
WITH prov_totals AS (
    SELECT
        province,
        SUM(per_capita_cad)                        AS total_per_capita
    FROM nhex
    WHERE year = (SELECT MAX(year) FROM nhex WHERE is_forecast = 0)
      AND is_forecast = 0
    GROUP BY province
),
nat AS (
    SELECT AVG(total_per_capita) AS national_avg FROM prov_totals
)
SELECT
    p.province,
    ROUND(p.total_per_capita, 0)                   AS per_capita,
    ROUND(p.total_per_capita - n.national_avg, 0)  AS vs_national,
    CASE WHEN p.total_per_capita > n.national_avg
         THEN 'Above Average' ELSE 'Below Average' END AS status
FROM prov_totals p
CROSS JOIN nat n
ORDER BY p.total_per_capita DESC;
