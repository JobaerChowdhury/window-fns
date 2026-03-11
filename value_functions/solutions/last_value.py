"""
solutions/last_value.py — LAST_VALUE() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the LAST_VALUE() exercises.
Refer to this file ONLY if you are stuck on exercises/last_value.py.

Running this file will verify all three solutions pass.

⚠️  Remember: LAST_VALUE() MUST have:
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
Without this frame clause the window only extends to the current row,
so LAST_VALUE() will equal the current row's value on every row.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_last_value_ex1, validate_last_value_ex2, validate_last_value_ex3

con = get_connection()

print_header(
    "LAST_VALUE() — Solutions",
    "Reference solutions — run to confirm all exercises pass. "
    "Don't forget the ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING frame!",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, show the StockCode of the LAST item the customer
# ever purchased. Every row for a customer should carry the same last_stockcode.
#
# Key idea: ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING is
#           REQUIRED so LAST_VALUE() can see beyond the current row to the end
#           of the partition.

user_sql_1 = """
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        StockCode,
        LAST_VALUE(StockCode) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_stockcode
    FROM retail_data
    WHERE CustomerID IS NOT NULL
"""


check_exercise(
    number=1,
    description="Show each customer's last-ever StockCode on every invoice row",
    user_sql=user_sql_1,
    validation_fn=validate_last_value_ex1,
    con=con,
    hint="LAST_VALUE(StockCode) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each StockCode in each Country, attach the price of the MOST EXPENSIVE
# StockCode in that Country (priciest_in_country).
#
# Key idea: ORDER BY avg_price ASC so the last row in the partition holds the
#           maximum — LAST_VALUE then picks that up on every row.

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
        LAST_VALUE(avg_price) OVER (
            PARTITION BY Country
            ORDER BY avg_price ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS priciest_in_country
    FROM avg_prices
"""


check_exercise(
    number=2,
    description="Attach each country's most expensive avg product price to every row",
    user_sql=user_sql_2,
    validation_fn=validate_last_value_ex2,
    con=con,
    hint="Aggregate AVG(UnitPrice) first, then LAST_VALUE(avg_price) OVER (PARTITION BY Country ORDER BY avg_price ASC ROWS UNBOUNDED ...)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each customer, show both their first and last purchase date on every
# invoice row, plus the total customer lifetime in days.
#
# Key idea: combine FIRST_VALUE and LAST_VALUE in the same query — both need
#           the full-frame clause. Compute lifetime_days with DATEDIFF.

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
        LAST_VALUE(invoice_day) OVER (
            PARTITION BY CustomerID
            ORDER BY invoice_day
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_purchase_day,
        DATEDIFF(
            'day',
            FIRST_VALUE(invoice_day) OVER (
                PARTITION BY CustomerID
                ORDER BY invoice_day
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ),
            LAST_VALUE(invoice_day) OVER (
                PARTITION BY CustomerID
                ORDER BY invoice_day
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            )
        ) AS lifetime_days
    FROM invoice_days
"""


check_exercise(
    number=3,
    description="Customer lifetime in days using FIRST_VALUE and LAST_VALUE together",
    user_sql=user_sql_3,
    validation_fn=validate_last_value_ex3,
    con=con,
    hint="FIRST_VALUE and LAST_VALUE both need ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING; subtract to get lifetime_days",
)
