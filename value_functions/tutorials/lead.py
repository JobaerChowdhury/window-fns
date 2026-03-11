"""
tutorials/lead.py — LEAD() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEAD() looks forward N rows within a window partition and returns the
value from that later row. It mirrors LAG() but peeks ahead instead of
behind — useful for computing time-to-next-event, next-period values, or
identifying what comes after the current row.

Syntax:
    LEAD(column [, offset [, default]])
        OVER ([PARTITION BY col, ...] ORDER BY col [ASC|DESC])

  offset  — how many rows to look ahead (default 1)
  default — value returned when no future row exists (default NULL)

Run this file:
    python tutorials/lead.py

Then head to exercises/lead.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "LEAD() — Peek Ahead at Future Rows",
    "LEAD() fetches a value from a future row within the same window. "
    "It is the mirror of LAG() and is ideal for computing the next event, "
    "time gaps, or lookahead comparisons.",
)


# ── Tutorial 1: Next invoice date per customer ───────────────────────────────
run_tutorial(
    title="Show each customer's next invoice date",
    description=(
        "LEAD(InvoiceDate, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) "
        "returns the date of the very next invoice for the same customer. "
        "The last purchase per customer returns NULL because there is no "
        "subsequent row."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            LEAD(InvoiceDate, 1) OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate
            ) AS next_invoice_date
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Days until next purchase ────────────────────────────────────
run_tutorial(
    title="Days until each customer's next purchase",
    description=(
        "Cast InvoiceDate to a DATE, then use LEAD() to fetch the next purchase "
        "date. Subtracting the two dates gives the gap in days. A NULL gap means "
        "the row is the customer's most recent purchase — there is no next one yet."
    ),
    sql="""
        WITH per_invoice AS (
            SELECT DISTINCT
                CustomerID,
                CAST(STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS DATE) AS invoice_day,
                InvoiceNo
            FROM retail_data
            WHERE CustomerID IS NOT NULL
        )
        SELECT
            CustomerID,
            invoice_day,
            InvoiceNo,
            LEAD(invoice_day) OVER (
                PARTITION BY CustomerID
                ORDER BY invoice_day
            ) AS next_invoice_day,
            DATEDIFF(
                'day',
                invoice_day,
                LEAD(invoice_day) OVER (
                    PARTITION BY CustomerID
                    ORDER BY invoice_day
                )
            ) AS days_until_next
        FROM per_invoice
        ORDER BY CustomerID, invoice_day
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Identify a customer's final purchase ────────────────────────
run_tutorial(
    title="Identify each customer's final purchase",
    description=(
        "When LEAD() returns NULL, there is no next row — meaning the current "
        "row is the last one for that partition. Filter WHERE next_invoice IS NULL "
        "to keep only each customer's most recent invoice. This is the LEAD() "
        "equivalent of the 'first purchase via ROW_NUMBER() = 1' pattern."
    ),
    sql="""
        WITH per_invoice AS (
            SELECT DISTINCT
                CustomerID,
                InvoiceDate,
                InvoiceNo,
                Country
            FROM retail_data
            WHERE CustomerID IS NOT NULL
        ),
        with_lead AS (
            SELECT
                CustomerID,
                InvoiceDate,
                InvoiceNo,
                Country,
                LEAD(InvoiceDate) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ) AS next_invoice_date
            FROM per_invoice
        )
        SELECT
            CustomerID,
            InvoiceDate AS last_invoice_date,
            InvoiceNo   AS last_invoice_no,
            Country
        FROM with_lead
        WHERE next_invoice_date IS NULL
        ORDER BY CustomerID
        LIMIT 20
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/lead.py\n")
