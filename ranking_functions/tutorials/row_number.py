"""
tutorials/row_number.py — ROW_NUMBER() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROW_NUMBER() assigns a unique, sequential integer to each row within a
window partition, starting at 1. No ties — every row gets a different number
even if their sort key is identical.

Syntax:
    ROW_NUMBER() OVER ([PARTITION BY col, ...] ORDER BY col [ASC|DESC])

Run this file:
    python tutorials/row_number.py

Then head to exercises/row_number.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "ROW_NUMBER() — Sequential Row Numbers",
    "ROW_NUMBER() numbers each row within a window partition from 1 upward. "
    "Unlike RANK(), it NEVER produces ties — two identical values get "
    "consecutive, distinct numbers.",
)


# ── Tutorial 1: Global row number ordered by date ────────────────────────────
run_tutorial(
    title="Assign a global row number ordered by date",
    description=(
        "The simplest use: number every row in the dataset from 1 to N, "
        "ordered by InvoiceDate. There is no PARTITION BY, so the window "
        "spans the entire table."
    ),
    sql="""
        SELECT
            ROW_NUMBER() OVER (ORDER BY InvoiceDate)  AS row_num,
            InvoiceDate,
            InvoiceNo,
            CustomerID,
            Description,
            Quantity
        FROM retail_data
        ORDER BY row_num
        LIMIT 20
    """,
    con=con,
)

# ── Tutorial 2: Number each customer's purchases in chronological order ───────
run_tutorial(
    title="Number each customer's purchases in order",
    description=(
        "Add PARTITION BY CustomerID so the counter resets to 1 for each "
        "customer. This tells us whether a given line is the customer's 1st, "
        "2nd, 3rd transaction, etc."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            Description,
            ROW_NUMBER() OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate 
            ) AS purchase_num
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, purchase_num
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Get each customer's very first purchase ─────────────────────
run_tutorial(
    title="Get each customer's very first purchase",
    description=(
        "Filter on purchase_num = 1 inside a CTE to keep only the first row "
        "per customer. This is one of the most common ROW_NUMBER() patterns "
        "in practice."
    ),
    sql="""
        WITH numbered AS (
            SELECT
                CustomerID,
                InvoiceDate,
                InvoiceNo,
                Description,
                Quantity,
                UnitPrice,
                ROW_NUMBER() OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ) AS purchase_num
            FROM retail_data
            WHERE CustomerID IS NOT NULL
        )
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            Description,
            Quantity,
            UnitPrice
        FROM numbered
        WHERE purchase_num = 1
        ORDER BY CustomerID
        LIMIT 20
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/row_number.py\n")
