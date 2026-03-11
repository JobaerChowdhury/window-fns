"""
tutorials/sum.py — SUM() OVER() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUM() OVER() computes a running or partitioned total without collapsing rows.
Unlike GROUP BY, every input row is preserved — the window is applied on top of
the full result set.

Syntax:
    SUM(expression)
        OVER ([PARTITION BY col, ...]
              [ORDER BY col [ASC|DESC]]
              [frame_clause])

  Without ORDER BY   → sums the entire partition (static total on every row)
  With ORDER BY      → running cumulative sum (default frame: UNBOUNDED PRECEDING
                       to CURRENT ROW)
  With frame_clause  → custom window (e.g. sliding 3-row moving average)

Run this file:
    python tutorials/sum.py

Then head to exercises/sum.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "SUM() OVER() — Running and Partitioned Totals",
    "SUM() OVER() lets you compute totals over a window of rows while "
    "keeping every individual row in the output. Combine it with "
    "PARTITION BY for group-level totals, ORDER BY for running sums, "
    "or a frame clause for moving totals.",
)


# ── Tutorial 1: Partition-level total revenue per country ───────────────────
run_tutorial(
    title="Total revenue per country attached to every row",
    description=(
        "SUM(Quantity * UnitPrice) OVER (PARTITION BY Country) computes the "
        "grand total revenue for each country and stamps that value onto every "
        "row belonging to that country. No ORDER BY means the entire partition "
        "is summed — the value is the same for every row in the same country."
    ),
    sql="""
        SELECT
            Country,
            InvoiceNo,
            InvoiceDate,
            ROUND(Quantity * UnitPrice, 2)                             AS line_revenue,
            ROUND(SUM(Quantity * UnitPrice) OVER (PARTITION BY Country), 2)
                                                                       AS country_total_revenue
        FROM retail_data
        WHERE Quantity > 0
        ORDER BY Country, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Running cumulative revenue per customer ─────────────────────
run_tutorial(
    title="Running cumulative spend per customer",
    description=(
        "Adding ORDER BY InvoiceDate turns SUM() into a running cumulative "
        "total. The default frame (UNBOUNDED PRECEDING TO CURRENT ROW) means "
        "each row's cumulative_spend includes all prior rows for that customer, "
        "showing how much the customer has spent up to and including each "
        "invoice date."
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
                SUM(invoice_revenue) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ),
                2
            ) AS cumulative_spend
        FROM invoice_totals
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Rolling 3-invoice revenue window per customer ───────────────
run_tutorial(
    title="3-invoice rolling revenue total per customer",
    description=(
        "A custom frame clause — ROWS BETWEEN 2 PRECEDING AND CURRENT ROW — "
        "limits SUM() to the current row plus the two rows before it (within "
        "the same CustomerID partition). This gives a 'last 3 invoices' rolling "
        "total, useful for detecting recent spend trends. When fewer than 3 "
        "prior rows exist the frame simply uses however many rows are available."
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
                SUM(invoice_revenue) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ),
                2
            ) AS rolling_3_revenue
        FROM invoice_totals
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/sum.py\n")
