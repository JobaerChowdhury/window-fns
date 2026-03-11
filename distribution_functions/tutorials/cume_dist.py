"""
tutorials/cume_dist.py — CUME_DIST() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CUME_DIST() returns the *cumulative distribution* of a value within its
partition — the fraction of rows with a value less than or equal to the
current row's value.

Syntax:
    CUME_DIST()
        OVER ([PARTITION BY col, ...]
               ORDER BY col [ASC|DESC])

Formula (for row i with ORDER BY ASC):
    CUME_DIST = (number of rows with value <= current row's value)
                ─────────────────────────────────────────────────
                            total rows in partition

Key facts:
  - Result is always in the range (0, 1] — the last row always = 1.0.
  - Ties share the SAME cumulative distance (the highest value for the tie group).
  - Multiply by 100 to express as a percentile (0–100).
  - No frame clause — CUME_DIST always considers the entire partition.

Compare with PERCENT_RANK:
  CUME_DIST  includes ties and always ends at 1.0.
  PERCENT_RANK excludes ties and the first value is always 0.0.

Run this file:
    python tutorials/cume_dist.py

Then head to exercises/cume_dist.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "CUME_DIST() — Cumulative Distribution",
    "CUME_DIST() tells you what fraction of rows in the partition have a "
    "value <= the current row's value. Think of it as a percentile rank "
    "where 1.0 = 100th percentile.",
)


# ── Tutorial 1: Country revenue cumulative distribution ─────────────────────
run_tutorial(
    title="Cumulative distribution of country revenue",
    description=(
        "CUME_DIST() OVER (ORDER BY country_revenue ASC) shows what fraction "
        "of countries earn less than or equal to this country's total revenue. "
        "A value of 0.85 means this country outperforms 85 % of all countries "
        "in the dataset. The last country (highest revenue) always gets 1.0."
    ),
    sql="""
        WITH country_rev AS (
            SELECT
                Country,
                ROUND(SUM(Quantity * UnitPrice), 2) AS country_revenue
            FROM retail_data
            WHERE Quantity > 0
            GROUP BY Country
        )
        SELECT
            Country,
            country_revenue,
            ROUND(CUME_DIST() OVER (ORDER BY country_revenue ASC), 4)
                AS cume_dist,
            ROUND(CUME_DIST() OVER (ORDER BY country_revenue ASC) * 100, 1)
                AS percentile
        FROM country_rev
        ORDER BY country_revenue
    """,
    con=con,
)

# ── Tutorial 2: Per-country product price cumulative distribution ───────────
run_tutorial(
    title="Product price cumulative distribution within each country",
    description=(
        "CUME_DIST() OVER (PARTITION BY Country ORDER BY avg_price ASC) "
        "computes the cumulative distribution independently for each country. "
        "A product with cume_dist = 0.5 is at the median for its country — "
        "50 % of that country's products are equally or less expensive. "
        "This is useful for country-relative price benchmarking."
    ),
    sql="""
        WITH product_prices AS (
            SELECT
                Country,
                StockCode,
                ROUND(AVG(UnitPrice), 2) AS avg_price
            FROM retail_data
            WHERE Quantity > 0 AND UnitPrice > 0
            GROUP BY Country, StockCode
        )
        SELECT
            Country,
            StockCode,
            avg_price,
            ROUND(
                CUME_DIST() OVER (
                    PARTITION BY Country
                    ORDER BY avg_price ASC
                ), 4
            ) AS cume_dist
        FROM product_prices
        WHERE Country IN ('United Kingdom', 'Germany', 'France')
        ORDER BY Country, avg_price
        LIMIT 30
    """,
    con=con,
)

# ── Tutorial 3: CUME_DIST vs PERCENT_RANK side-by-side ─────────────────────
run_tutorial(
    title="CUME_DIST vs PERCENT_RANK — spot the difference",
    description=(
        "This tutorial places CUME_DIST and PERCENT_RANK side-by-side on the "
        "same data to highlight their differences. PERCENT_RANK always starts "
        "at 0.0 and the first distinct value has a unique 0.0 rank. CUME_DIST "
        "always ends at 1.0 and ties share the HIGHEST fractional value in the "
        "group. In this query we rank customers by total spend so tied customers "
        "show the effect clearly."
    ),
    sql="""
        WITH customer_spend AS (
            SELECT
                CustomerID,
                ROUND(SUM(Quantity * UnitPrice), 2) AS total_spend
            FROM retail_data
            WHERE CustomerID IS NOT NULL AND Quantity > 0
            GROUP BY CustomerID
        )
        SELECT
            CustomerID,
            total_spend,
            ROUND(CUME_DIST()    OVER (ORDER BY total_spend ASC), 4) AS cume_dist,
            ROUND(PERCENT_RANK() OVER (ORDER BY total_spend ASC), 4) AS pct_rank
        FROM customer_spend
        ORDER BY total_spend
        LIMIT 20
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/cume_dist.py\n")
