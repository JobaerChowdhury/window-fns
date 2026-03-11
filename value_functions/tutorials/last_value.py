"""
tutorials/last_value.py — LAST_VALUE() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAST_VALUE() returns the value from the last row of the current window
frame. The key gotcha: the default frame is RANGE BETWEEN UNBOUNDED
PRECEDING AND CURRENT ROW, which means "last" is the current row itself
on most rows. To get the true last value in the partition you must
explicitly set the frame to ROWS BETWEEN UNBOUNDED PRECEDING AND
UNBOUNDED FOLLOWING.

Syntax:
    LAST_VALUE(column) OVER (
        [PARTITION BY col, ...]
        ORDER BY col [ASC|DESC]
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    )

Run this file:
    python tutorials/last_value.py

Then head to exercises/last_value.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "LAST_VALUE() — Get the Last Row in a Window",
    "LAST_VALUE() pins the partition's last-ordered value to every row. "
    "Always use 'ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING' "
    "or you will get the current row's own value instead of the true last.",
)


# ── Tutorial 1: Last product each customer bought ────────────────────────────
run_tutorial(
    title="Show each customer's most recent product on every invoice line",
    description=(
        "LAST_VALUE(Description) with the full frame clause returns the "
        "very last Description for each customer (ordered by date). Every "
        "row for that customer will show the same 'most recent' product, "
        "which is useful for labelling historical rows with the latest activity."
    ),
    sql="""
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            Description,
            LAST_VALUE(Description) OVER (
                PARTITION BY CustomerID
                ORDER BY InvoiceDate
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS most_recent_product
        FROM retail_data
        WHERE CustomerID IS NOT NULL
        ORDER BY CustomerID, InvoiceDate
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 2: Most expensive product per country ───────────────────────────
run_tutorial(
    title="Attach the priciest product in each country to every row",
    description=(
        "Sort by avg_price ASC and use LAST_VALUE() with the full frame. "
        "The last value in ascending order is the highest price, so every "
        "row in the country partition gets the maximum avg_price attached — "
        "without a GROUP BY or subquery."
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
            LAST_VALUE(avg_price) OVER (
                PARTITION BY Country
                ORDER BY avg_price ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS most_expensive_in_country
        FROM country_prices
        ORDER BY Country, avg_price
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: FIRST_VALUE vs LAST_VALUE side-by-side ──────────────────────
run_tutorial(
    title="FIRST_VALUE vs LAST_VALUE side-by-side: cheapest and priciest per country",
    description=(
        "Combine both functions in one query to show, for each product row, "
        "the cheapest and most expensive average price within its Country. "
        "This side-by-side pattern is handy for range/spread analysis and "
        "clearly illustrates both functions at once."
    ),
    sql="""
        WITH country_prices AS (
            SELECT
                Country,
                StockCode,
                ROUND(AVG(UnitPrice), 2) AS avg_price
            FROM retail_data
            WHERE UnitPrice > 0
            GROUP BY Country, StockCode
        )
        SELECT
            Country,
            StockCode,
            avg_price,
            FIRST_VALUE(avg_price) OVER (
                PARTITION BY Country
                ORDER BY avg_price ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS cheapest_price,
            LAST_VALUE(avg_price) OVER (
                PARTITION BY Country
                ORDER BY avg_price ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS priciest_price,
            ROUND(
                LAST_VALUE(avg_price) OVER (
                    PARTITION BY Country
                    ORDER BY avg_price ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                ) - FIRST_VALUE(avg_price) OVER (
                    PARTITION BY Country
                    ORDER BY avg_price ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                ),
                2
            ) AS price_range
        FROM country_prices
        ORDER BY Country, avg_price
        LIMIT 25
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/last_value.py\n")
