"""
tutorials/avg.py — AVG() OVER() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AVG() OVER() computes an average over a window without collapsing rows. It is
identical in behavior to SUM() OVER() but divides by the number of rows in
the window rather than summing them.

Syntax:
    AVG(expression)
        OVER ([PARTITION BY col, ...]
              [ORDER BY col [ASC|DESC]]
              [frame_clause])

  Without ORDER BY   → average over the entire partition (benchmark value)
  With ORDER BY      → running cumulative average
  With frame_clause  → moving/sliding average (e.g. last N rows)

Run this file:
    python tutorials/avg.py

Then head to exercises/avg.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "AVG() OVER() — Partition and Moving Averages",
    "AVG() OVER() lets you attach an average to every row without losing "
    "row-level detail. Use PARTITION BY to benchmark each row against its "
    "group average, ORDER BY for cumulative averages, or a frame clause "
    "for moving averages.",
)


# ── Tutorial 1: Average unit price per country as a benchmark ───────────────
run_tutorial(
    title="Benchmark each product's price against its country's average",
    description=(
        "AVG(UnitPrice) OVER (PARTITION BY Country) places the country-wide "
        "average unit price on every row. You can immediately compare each "
        "line item's UnitPrice to that baseline — a positive price_vs_avg "
        "means the item is pricier than average for its country."
    ),
    sql="""
        SELECT
            Country,
            Description,
            StockCode,
            ROUND(UnitPrice, 2)                                        AS unit_price,
            ROUND(AVG(UnitPrice) OVER (PARTITION BY Country), 2)       AS avg_price_country,
            ROUND(UnitPrice - AVG(UnitPrice) OVER (PARTITION BY Country), 2)
                                                                       AS price_vs_avg
        FROM retail_data
        WHERE UnitPrice > 0
        ORDER BY Country, UnitPrice DESC
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Running average invoice value per customer ──────────────────
run_tutorial(
    title="Running average invoice value per customer",
    description=(
        "AVG(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) "
        "computes a running cumulative average across a customer's invoices in "
        "date order. As new invoices are added the average updates, letting you "
        "see whether each new purchase is above or below the customer's current "
        "average spend."
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
                AVG(invoice_revenue) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ),
                2
            ) AS running_avg_spend
        FROM invoice_totals
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: 3-invoice moving average per customer ──────────────────────
run_tutorial(
    title="3-invoice moving average spend per customer",
    description=(
        "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW limits the average window "
        "to the current invoice and the two immediately before it. This 3-point "
        "moving average smooths out one-off spikes, making it easier to spot "
        "trends in customer spend behaviour. Compare it against the static "
        "partition average (avg_all_time) to see where each customer is "
        "currently trending."
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
            ROUND(AVG(invoice_revenue) OVER (PARTITION BY CustomerID), 2)
                AS avg_all_time,
            ROUND(
                AVG(invoice_revenue) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ),
                2
            ) AS moving_avg_3
        FROM invoice_totals
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/avg.py\n")
