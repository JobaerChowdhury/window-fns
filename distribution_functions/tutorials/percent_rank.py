"""
tutorials/percent_rank.py — PERCENT_RANK() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERCENT_RANK() returns the *relative standing* of a row within its
partition on a 0.0–1.0 scale.

Syntax:
    PERCENT_RANK()
        OVER ([PARTITION BY col, ...]
               ORDER BY col [ASC|DESC])

Formula:
    PERCENT_RANK = (RANK() - 1) / (total rows in partition - 1)

Key facts:
  - The first row (lowest ORDER BY value, ASC) always returns 0.0.
  - The last row (highest ORDER BY value, ASC) always returns 1.0.
  - Tied rows share the same PERCENT_RANK value (the lowest for the tie group).
  - For a single-row partition, PERCENT_RANK = 0.0.
  - Multiply by 100 to express as a 0–100 percentile.

Compare with CUME_DIST:
  PERCENT_RANK  uses rank-based formula; first value = 0.0; ties = lowest value.
  CUME_DIST     uses count-based formula; last value = 1.0; ties = highest value.

Run this file:
    python tutorials/percent_rank.py

Then head to exercises/percent_rank.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "PERCENT_RANK() — Relative Rank as a Fraction",
    "PERCENT_RANK() maps each row's rank onto a 0.0–1.0 scale using the "
    "formula (RANK - 1) / (N - 1). The lowest-ranked row is always 0.0 "
    "and the highest is always 1.0.",
)


# ── Tutorial 1: Customer spend percent rank ─────────────────────────────────
run_tutorial(
    title="Customer spend percent rank (global)",
    description=(
        "PERCENT_RANK() OVER (ORDER BY total_spend ASC) shows the relative "
        "standing of each customer in the global spend distribution. A "
        "percent_rank of 0.95 means this customer spends more than 95 % of "
        "all customers. The first (lowest-spend) customer always has "
        "percent_rank = 0.0; the top spender has 1.0."
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
            ROUND(PERCENT_RANK() OVER (ORDER BY total_spend ASC), 4)
                AS percent_rank,
            ROUND(PERCENT_RANK() OVER (ORDER BY total_spend ASC) * 100, 1)
                AS percentile
        FROM customer_spend
        ORDER BY total_spend DESC
        LIMIT 20
    """,
    con=con,
)

# ── Tutorial 2: Per-country product rank ───────────────────────────────────
run_tutorial(
    title="Product avg-price percent rank within each country",
    description=(
        "PERCENT_RANK() OVER (PARTITION BY Country ORDER BY avg_price ASC) "
        "independently ranks products by average price within each country "
        "on a 0–1 scale. A product at percent_rank = 0.9 is in the top "
        "10 % most expensive products in its country. The PARTITION BY "
        "resets the 0.0–1.0 scale for every country."
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
                PERCENT_RANK() OVER (
                    PARTITION BY Country
                    ORDER BY avg_price ASC
                ), 4
            ) AS percent_rank
        FROM product_prices
        WHERE Country IN ('United Kingdom', 'Germany', 'France')
        ORDER BY Country, avg_price DESC
        LIMIT 30
    """,
    con=con,
)

# ── Tutorial 3: NTILE, CUME_DIST, PERCENT_RANK side-by-side ────────────────
run_tutorial(
    title="NTILE, CUME_DIST, and PERCENT_RANK — all three together",
    description=(
        "This tutorial puts all three distribution functions side-by-side on "
        "country revenue data. NTILE(4) assigns a discrete bucket (1–4). "
        "CUME_DIST shows the fraction of countries at or below this revenue "
        "(includes ties at the top of each tie group). PERCENT_RANK shows "
        "the rank-based relative position (ties at the bottom of each tie "
        "group; first value = 0.0). Comparing the three columns reveals how "
        "each function handles ties differently."
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
            NTILE(4)       OVER (ORDER BY country_revenue ASC) AS ntile_quartile,
            ROUND(CUME_DIST()    OVER (ORDER BY country_revenue ASC), 4) AS cume_dist,
            ROUND(PERCENT_RANK() OVER (ORDER BY country_revenue ASC), 4) AS pct_rank
        FROM country_rev
        ORDER BY country_revenue
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/percent_rank.py\n")
