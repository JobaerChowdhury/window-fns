"""
tutorials/min.py — MIN() OVER() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MIN() OVER() finds the minimum value within a window partition and attaches it
to every row in that partition, without collapsing the result set.

Syntax:
    MIN(expression)
        OVER ([PARTITION BY col, ...]
              [ORDER BY col [ASC|DESC]]
              [frame_clause])

  Without ORDER BY   → global minimum of the entire partition
  With ORDER BY      → running minimum (lowest value seen so far)
  With frame clause  → minimum within a sliding window

Run this file:
    python tutorials/min.py

Then head to exercises/min.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "MIN() OVER() — Partition and Running Minimums",
    "MIN() OVER() stamps the minimum value from a window onto every row. "
    "Great for benchmarking (cheapest price in a country), detecting the "
    "historical lowest point, or finding the first event date without a "
    "self-join.",
)


# ── Tutorial 1: Cheapest product price per country on every row ─────────────
run_tutorial(
    title="Show the cheapest product price per country on every row",
    description=(
        "MIN(UnitPrice) OVER (PARTITION BY Country) places the lowest unit "
        "price found in each country onto every row for that country. This "
        "lets you compare each item's price against the country floor in a "
        "single query — price_vs_min shows how much more expensive an item "
        "is than the cheapest option in the same market."
    ),
    sql="""
        SELECT
            Country,
            StockCode,
            Description,
            ROUND(UnitPrice, 2)                                          AS unit_price,
            ROUND(MIN(UnitPrice) OVER (PARTITION BY Country), 2)        AS min_price_country,
            ROUND(UnitPrice - MIN(UnitPrice) OVER (PARTITION BY Country), 2)
                                                                         AS price_vs_min
        FROM retail_data
        WHERE UnitPrice > 0
        ORDER BY Country, UnitPrice
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Running minimum spend per customer ──────────────────────────
run_tutorial(
    title="Running cheapest invoice per customer (historical floor)",
    description=(
        "MIN(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) "
        "builds a running minimum: as we step through each invoice in date order "
        "the value can only stay the same or decrease. This 'cheapest so far' "
        "baseline is useful for detecting when a customer spends unusually little "
        "compared to their history."
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
                MIN(invoice_revenue) OVER (
                    PARTITION BY CustomerID
                    ORDER BY InvoiceDate
                ),
                2
            ) AS running_min_spend
        FROM invoice_totals
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Earliest invoice date per customer on every row ─────────────
run_tutorial(
    title="Earliest purchase date per customer (acquisition date)",
    description=(
        "MIN() works on any orderable type, including dates. "
        "MIN(InvoiceDate) OVER (PARTITION BY CustomerID) retrieves each "
        "customer's very first invoice date and stamps it on every row. "
        "This 'acquisition date' sidesteps the need for a JOIN or subquery "
        "and makes it trivial to compute days_since_first_purchase inline."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            MIN(InvoiceDate) OVER (PARTITION BY CustomerID) AS first_purchase_date,
            DATEDIFF(
                'day',
                STRPTIME(MIN(InvoiceDate) OVER (PARTITION BY CustomerID), '%m/%d/%Y %H:%M'),
                STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M')
            ) AS days_since_first_purchase
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/min.py\n")
