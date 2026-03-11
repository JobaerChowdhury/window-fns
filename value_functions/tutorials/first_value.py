"""
tutorials/first_value.py — FIRST_VALUE() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIRST_VALUE() returns the value from the very first row of the window
frame. Combined with PARTITION BY, it lets you attach a group's "baseline"
value to every row in that group — without a join or subquery.

Syntax:
    FIRST_VALUE(column) OVER (
        [PARTITION BY col, ...]
        ORDER BY col [ASC|DESC]
        [ROWS/RANGE BETWEEN ...]   -- frame clause (optional)
    )

Important: By default the frame is RANGE BETWEEN UNBOUNDED PRECEDING AND
CURRENT ROW, so FIRST_VALUE() reliably returns the partition's very first
ordered value.

Run this file:
    python tutorials/first_value.py

Then head to exercises/first_value.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "FIRST_VALUE() — Get the First Row in a Window",
    "FIRST_VALUE() pins the very first value in a partition's ordering to "
    "every row. It is ideal for 'compare each row to the group baseline' "
    "scenarios — first price, first date, first product, etc.",
)


# ── Tutorial 1: First product each customer ever bought ──────────────────────
run_tutorial(
    title="Show each customer's first-ever product on every invoice line",
    description=(
        "FIRST_VALUE(Description) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) "
        "returns the Description from the customer's earliest invoice across ALL "
        "their invoice lines — so every row for that customer carries the same "
        "first-ever product name."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            Description,
            FIRST_VALUE(Description) OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS first_product_ever
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Cheapest unit price per country (baseline comparison) ────────
run_tutorial(
    title="Compare each product's price to the cheapest price in its country",
    description=(
        "Aggregate average UnitPrice per (Country, StockCode), then use "
        "FIRST_VALUE() ordered by avg_price ASC to get the cheapest product "
        "per country. Subtract to find how much more expensive each item is "
        "compared to the country's cheapest offering."
    ),
    sql="""
        WITH country_prices AS (
            SELECT
                Country,
                StockCode,
                Description,
                ROUND(AVG(UnitPrice), 2) AS avg_price
            FROM retail_data
            WHERE UnitPrice > 0
            GROUP BY Country, StockCode, Description
        )
        SELECT
            Country,
            StockCode,
            Description,
            avg_price,
            FIRST_VALUE(avg_price) OVER (
                PARTITION BY Country
                ORDER BY avg_price ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS cheapest_in_country,
            ROUND(
                avg_price - FIRST_VALUE(avg_price) OVER (
                    PARTITION BY Country
                    ORDER BY avg_price ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                ),
                2
            ) AS price_above_cheapest
        FROM country_prices
        ORDER BY Country, avg_price
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: First invoice date vs current date gap ──────────────────────
run_tutorial(
    title="Days since a customer's very first purchase",
    description=(
        "FIRST_VALUE() on the invoice date (ordered ASC) gives the absolute "
        "first purchase date for each customer. Combining that with the current "
        "row's date lets us compute 'days since first purchase' — a simple "
        "customer tenure metric present on every row."
    ),
    sql="""
        WITH dated AS (
            SELECT
                CustomerID,
                InvoiceNo,
                CAST(STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS DATE) AS invoice_day
            FROM retail_data
            WHERE CustomerID IS NOT NULL
        )
        SELECT
            CustomerID,
            invoice_day,
            InvoiceNo,
            FIRST_VALUE(invoice_day) OVER (
                PARTITION BY CustomerID
                ORDER BY invoice_day
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS first_purchase_day,
            DATEDIFF(
                'day',
                FIRST_VALUE(invoice_day) OVER (
                    PARTITION BY CustomerID
                    ORDER BY invoice_day
                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                ),
                invoice_day
            ) AS days_since_first_purchase
        FROM dated
        ORDER BY CustomerID, invoice_day DESC 
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/first_value.py\n")
