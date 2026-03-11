"""
tutorials/count.py — COUNT() OVER() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COUNT() OVER() counts rows (or non-NULL values of a column) within a window
partition without collapsing rows. It pairs naturally with PARTITION BY to
produce group-level counts on every detail row.

Syntax:
    COUNT(* | expression)
        OVER ([PARTITION BY col, ...]
              [ORDER BY col [ASC|DESC]]
              [frame_clause])

  COUNT(*)              → counts all rows in the window (including NULLs)
  COUNT(column)         → counts non-NULL values in the window
  Without ORDER BY      → static count for the entire partition
  With ORDER BY         → running count (rows seen so far)

Run this file:
    python tutorials/count.py

Then head to exercises/count.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "COUNT() OVER() — Partition and Running Counts",
    "COUNT() OVER() lets you count rows within a group while keeping every "
    "individual row visible. Use it to add group sizes, running row counts, "
    "or to flag rows where a customer has made many purchases.",
)


# ── Tutorial 1: Number of invoices per customer on every row ────────────────
run_tutorial(
    title="Show each customer's total invoice count on every row",
    description=(
        "COUNT(InvoiceNo) OVER (PARTITION BY CustomerID) counts the distinct "
        "events per customer and repeats that count on every row. This is "
        "ideal for filtering — e.g. WHERE total_invoices > 5 — without a "
        "separate subquery. Note: COUNT() here counts rows, not distinct IDs."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceNo,
            InvoiceDate,
            Country,
            COUNT(InvoiceNo) OVER (PARTITION BY CustomerID) AS total_invoice_rows
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Running count of purchase events per customer ───────────────
run_tutorial(
    title="Running purchase-event counter per customer",
    description=(
        "Adding ORDER BY InvoiceDate makes COUNT() accumulate row by row. "
        "invoice_seq tells you how many line-item rows this customer has "
        "generated up to and including the current row. It is a simpler "
        "alternative to ROW_NUMBER() when you want an event tally rather "
        "than a sequential rank."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            StockCode,
            COUNT(*) OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate
            ) AS invoice_seq
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Count non-NULL CustomerIDs per country (presence check) ─────
run_tutorial(
    title="Country coverage — count known customers per country",
    description=(
        "COUNT(CustomerID) OVER (PARTITION BY Country) counts only non-NULL "
        "CustomerID values per country, showing how many rows have an identified "
        "customer. Rows where CustomerID IS NULL are excluded from the count but "
        "still appear in the result. This is a quick data-quality check to see "
        "which countries have high proportions of anonymous orders."
    ),
    sql="""
        SELECT
            Country,
            InvoiceNo,
            CustomerID,
            COUNT(CustomerID) OVER (PARTITION BY Country)   AS known_customer_rows,
            COUNT(*)          OVER (PARTITION BY Country)   AS total_rows,
            ROUND(
                100.0 * COUNT(CustomerID) OVER (PARTITION BY Country)
                      / COUNT(*)          OVER (PARTITION BY Country),
                1
            )                                               AS pct_identified
        FROM retail_data
        ORDER BY Country, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/count.py\n")
