"""
solutions/first_value.py — FIRST_VALUE() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the FIRST_VALUE() exercises.
Refer to this file ONLY if you are stuck on exercises/first_value.py.

Running this file will verify all three solutions pass.

⚠️  Remember: to avoid the default "rows up to current row" frame, always use
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_first_value_ex1, validate_first_value_ex2, validate_first_value_ex3

con = get_connection()

print_header(
    "FIRST_VALUE() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, show the StockCode of the FIRST item the customer
# ever purchased. Every row for a customer should carry the same first_stockcode.
#
# Key idea: ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING ensures
#           FIRST_VALUE() sees the entire partition, not just up to the current row.

user_sql_1 = """
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        StockCode,
        FIRST_VALUE(StockCode) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_stockcode
    FROM retail_data
    WHERE CustomerID IS NOT NULL
"""


check_exercise(
    number=1,
    description="Show the first-ever StockCode purchased by each customer on every row",
    user_sql=user_sql_1,
    validation_fn=validate_first_value_ex1,
    con=con,
    hint="FIRST_VALUE(StockCode) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each StockCode in each Country, attach the price of the CHEAPEST
# StockCode in that Country (cheapest_in_country).
#
# Key idea: aggregate AVG(UnitPrice) per (Country, StockCode) first,
#           then ORDER BY avg_price ASC so FIRST_VALUE picks the lowest price.

user_sql_2 = """
    WITH avg_prices AS (
        SELECT
            Country,
            StockCode,
            AVG(UnitPrice) AS avg_price
        FROM retail_data
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
        ) AS cheapest_in_country
    FROM avg_prices
"""


check_exercise(
    number=2,
    description="Attach each country's cheapest avg product price to every row",
    user_sql=user_sql_2,
    validation_fn=validate_first_value_ex2,
    con=con,
    hint="Aggregate AVG(UnitPrice) first, then FIRST_VALUE(avg_price) OVER (PARTITION BY Country ORDER BY avg_price ASC ROWS UNBOUNDED ...)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Find the time elapsed (in days) from each customer's very first purchase
# to every subsequent purchase.
#
# Key idea: parse InvoiceDate with STRPTIME, cast to DATE in a CTE,
#           then FIRST_VALUE(invoice_day) with the full frame yields the very
#           first date regardless of current row position.

user_sql_3 = """
    WITH invoice_days AS (
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
        ) AS days_since_first
    FROM invoice_days
"""


check_exercise(
    number=3,
    description="Days elapsed since each customer's first-ever purchase",
    user_sql=user_sql_3,
    validation_fn=validate_first_value_ex3,
    con=con,
    hint="FIRST_VALUE(invoice_day) OVER (...) AS first_purchase_day, then DATEDIFF('day', first_purchase_day, invoice_day)",
)
