"""
tutorials/ntile.py — NTILE() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NTILE(n) divides an ordered partition into n roughly equal buckets and
assigns each row a bucket number from 1 to n.  It is useful for
quartile/quintile/decile analysis — e.g. "which spend quartile does
this customer fall into?"

Syntax:
    NTILE(n)
        OVER ([PARTITION BY col, ...]
               ORDER BY col [ASC|DESC])

  n           → number of buckets (integer literal or expression)
  ORDER BY    → required — determines the ordering within each partition
                before bucket assignment
  PARTITION BY → optional — applies NTILE independently per group

Key behaviour:
  - If the number of rows is not divisible by n, the larger buckets come
    FIRST (bucket 1, 2, ... get the extra row).
  - Bucket 1 = lowest-ranked rows (when ORDER BY ASC).
  - No frame clause is meaningful — NTILE always looks at the full partition.

Run this file:
    python tutorials/ntile.py

Then head to exercises/ntile.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "NTILE() — Bucket / Quartile Analysis",
    "NTILE(n) splits an ordered set of rows into n equal-sized buckets "
    "and labels each row with its bucket number (1 = first bucket). "
    "Use it for quartile, quintile, or decile segmentation.",
)


# ── Tutorial 1: Quartile revenue buckets per country ───────────────────────
run_tutorial(
    title="Revenue quartiles across all countries",
    description=(
        "NTILE(4) OVER (ORDER BY country_revenue ASC) divides countries "
        "into four equal groups by total revenue. Bucket 1 contains the "
        "lowest-revenue countries and bucket 4 the highest. Each country "
        "gets a quartile label attached to every one of its rows — no GROUP "
        "BY is needed."
    ),
    sql="""
        WITH country_revenue AS (
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
            NTILE(4) OVER (ORDER BY country_revenue ASC) AS revenue_quartile
        FROM country_revenue
        ORDER BY revenue_quartile, country_revenue
    """,
    con=con,
)

# ── Tutorial 2: Per-country product price deciles ──────────────────────────
run_tutorial(
    title="Product price deciles within each country",
    description=(
        "NTILE(10) OVER (PARTITION BY Country ORDER BY avg_price ASC) "
        "independently divides products within each country into 10 equal "
        "price buckets. Decile 1 = the cheapest 10 % of products in that "
        "country; decile 10 = the most expensive 10 %. The PARTITION BY "
        "ensures each country gets its own 1–10 scale."
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
            NTILE(10) OVER (
                PARTITION BY Country
                ORDER BY avg_price ASC
            ) AS price_decile
        FROM product_prices
        ORDER BY Country, price_decile, avg_price
        LIMIT 30
    """,
    con=con,
)

# ── Tutorial 3: Customer spend quintiles + label ────────────────────────────
run_tutorial(
    title="Customer spend quintiles with human-readable labels",
    description=(
        "NTILE(5) splits customers into five equal spend buckets. A CASE "
        "expression then converts bucket numbers into descriptive labels "
        "(Bronze → Platinum). This pattern is common in marketing analysis "
        "— once you have the quintile number, you can join it to any "
        "downstream table or CRM without re-running the window function."
    ),
    sql="""
        WITH customer_spend AS (
            SELECT
                CustomerID,
                ROUND(SUM(Quantity * UnitPrice), 2) AS total_spend
            FROM retail_data
            WHERE CustomerID IS NOT NULL AND Quantity > 0
            GROUP BY CustomerID
        ), with_quintile AS (
            SELECT
                CustomerID,
                total_spend,
                NTILE(5) OVER (ORDER BY total_spend ASC) AS spend_quintile
            FROM customer_spend
        )
        SELECT
            CustomerID,
            total_spend,
            spend_quintile,
            CASE spend_quintile
                WHEN 1 THEN 'Bronze'
                WHEN 2 THEN 'Silver'
                WHEN 3 THEN 'Gold'
                WHEN 4 THEN 'Platinum'
                WHEN 5 THEN 'Diamond'
            END AS spend_tier
        FROM with_quintile
        ORDER BY spend_quintile, total_spend
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/ntile.py\n")
