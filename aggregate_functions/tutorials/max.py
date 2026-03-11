"""
tutorials/max.py — MAX() OVER() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MAX() OVER() finds the maximum value within a window partition and attaches it
to every row in the partition, without collapsing rows.

Syntax:
    MAX(expression)
        OVER ([PARTITION BY col, ...]
              [ORDER BY col [ASC|DESC]]
              [frame_clause])

  Without ORDER BY   → global maximum of the entire partition
  With ORDER BY      → running maximum (highest value seen so far)
  With frame clause  → maximum within a sliding window

Run this file:
    python tutorials/max.py

Then head to exercises/max.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "MAX() OVER() — Partition and Running Maximums",
    "MAX() OVER() stamps the maximum value from a window onto every row. "
    "Use it to find the top price in a group, track the best-ever spend per "
    "customer, or identify the most recent date in a partition — all without "
    "collapsing the result set.",
)


# ── Tutorial 1: Most expensive product per country on every row ─────────────
run_tutorial(
    title="Show the priciest product per country on every row",
    description=(
        "MAX(UnitPrice) OVER (PARTITION BY Country) places the highest unit "
        "price of any product in a country onto every row from that country. "
        "The derived column pct_of_max shows what percentage of the country "
        "ceiling each item's price represents — handy for relative positioning "
        "without a separate aggregation step."
    ),
    sql="""
        SELECT
            Country,
            StockCode,
            Description,
            ROUND(UnitPrice, 2)                                          AS unit_price,
            ROUND(MAX(UnitPrice) OVER (PARTITION BY Country), 2)        AS max_price_country,
            ROUND(
                100.0 * UnitPrice / NULLIF(MAX(UnitPrice) OVER (PARTITION BY Country), 0),
                1
            )                                                            AS pct_of_max
        FROM retail_data
        WHERE UnitPrice > 0
        ORDER BY Country, UnitPrice DESC
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Running maximum invoice spend per customer ──────────────────
run_tutorial(
    title="Running highest invoice per customer (personal best spend)",
    description=(
        "MAX(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) "
        "produces a running maximum that can only stay flat or increase as we "
        "step forward in time. This 'best invoice so far' benchmark shows whether "
        "the current invoice is a new personal spending high for the customer."
    ),
    sql="""
        WITH invoice_totals AS (
            SELECT
                CustomerID,
                InvoiceNo,
                InvoiceDate,
                ROUND(SUM(Quantity * UnitPrice), 2) AS invoice_revenue
            FROM retail_data
            WHERE CustomerID IS NOT NULL
              AND Quantity > 0
            GROUP BY CustomerID, InvoiceNo, InvoiceDate
        )
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            invoice_revenue,
            ROUND(
                MAX(invoice_revenue) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ),
                2
            ) AS running_max_spend,
            CASE
                WHEN invoice_revenue = MAX(invoice_revenue) OVER (
                    PARTITION BY CustomerID ORDER BY InvoiceDate
                ) THEN 'new personal best 🏆'
                ELSE ''
            END AS is_new_max
        FROM invoice_totals
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Top quantity sold per StockCode in each country ─────────────
run_tutorial(
    title="Max quantity per StockCode per country — identify blockbusters",
    description=(
        "MAX(Quantity) OVER (PARTITION BY Country, StockCode) stamps the "
        "single largest quantity ever sold for a given product in a given "
        "country onto every matching row. Rows where the current Quantity "
        "equals max_quantity_in_country are the 'blockbuster' transactions. "
        "This is a clean alternative to a correlated subquery."
    ),
    sql="""
        SELECT
            Country,
            StockCode,
            Description,
            InvoiceNo,
            Quantity,
            MAX(Quantity) OVER (PARTITION BY Country, StockCode) AS max_quantity_in_country,
            CASE
                WHEN Quantity = MAX(Quantity) OVER (PARTITION BY Country, StockCode)
                THEN 'peak sale ⭐'
                ELSE ''
            END AS is_peak
        FROM retail_data
        WHERE Quantity > 0
        ORDER BY Country, StockCode, Quantity DESC
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/max.py\n")
