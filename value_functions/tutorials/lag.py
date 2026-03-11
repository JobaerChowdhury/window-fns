"""
tutorials/lag.py — LAG() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAG() looks back N rows within a window partition and returns the value
from that earlier row. It is perfect for comparing a row's value to its
predecessor — e.g. month-over-month change, previous purchase amount, etc.

Syntax:
    LAG(column [, offset [, default]])
        OVER ([PARTITION BY col, ...] ORDER BY col [ASC|DESC])

  offset  — how many rows to look back (default 1)
  default — value returned when no prior row exists (default NULL)

Run this file:
    python tutorials/lag.py

Then head to exercises/lag.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "LAG() — Look Back at Previous Rows",
    "LAG() fetches a value from a previous row within the same window. "
    "It is the go-to function for period-over-period comparisons and "
    "detecting changes between consecutive events.",
)


# ── Tutorial 1: Previous invoice date per customer ───────────────────────────
run_tutorial(
    title="Show each customer's previous invoice date",
    description=(
        "LAG(InvoiceDate, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) "
        "fetches the date of the row that came just before the current one for "
        "the same customer. The first purchase per customer returns NULL because "
        "there is no prior row."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            LAG(InvoiceDate, 1) OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate
            ) AS prev_invoice_date
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Revenue change between consecutive invoices ──────────────────
run_tutorial(
    title="Calculate revenue change between consecutive invoices",
    description=(
        "Aggregate total revenue per invoice, then use LAG() to pull the "
        "previous invoice's revenue. Subtracting gives the delta — positive "
        "means the customer spent more; negative means less. A default of 0 "
        "is supplied so the very first invoice shows a 0 delta instead of NULL."
    ),
    sql="""
        WITH invoice_revenue AS (
            SELECT
                CustomerID,
                InvoiceNo,
                InvoiceDate,
                ROUND(SUM(Quantity * UnitPrice), 2) AS revenue
            FROM retail_data
            WHERE CustomerID IS NOT NULL
              AND Quantity > 0
            GROUP BY CustomerID, InvoiceNo, InvoiceDate
        )
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            revenue,
            LAG(revenue, 1, 0) OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate
            ) AS prev_revenue,
            ROUND(
                revenue - LAG(revenue, 1, 0) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ),
                2
            ) AS revenue_delta
        FROM invoice_revenue
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Detect consecutive same-country orders ──────────────────────
run_tutorial(
    title="Detect when a customer places back-to-back orders from the same country",
    description=(
        "Use LAG() to compare each invoice's Country against the previous "
        "invoice's Country for the same customer. When they match the customer "
        "placed consecutive orders from the same location. This pattern is "
        "commonly used to detect streaks or stable behaviour."
    ),
    sql="""
        WITH per_invoice AS (
            SELECT DISTINCT
                CustomerID,
                InvoiceNo,
                InvoiceDate,
                Country
            FROM retail_data
            WHERE CustomerID IS NOT NULL
        )
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            Country,
            LAG(Country) OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate
            ) AS prev_country,
            CASE
                WHEN LAG(Country) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ) = Country THEN 'same'
                ELSE 'different'
            END AS country_streak
        FROM per_invoice
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/lag.py\n")
