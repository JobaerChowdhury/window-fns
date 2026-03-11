"""
solutions/max.py — MAX() OVER() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the MAX() OVER() exercises.
Refer to this file ONLY if you are stuck on exercises/max.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_max_ex1, validate_max_ex2, validate_max_ex3

con = get_connection()

print_header(
    "MAX() OVER() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each row, show the maximum UnitPrice globally and per Country.
#
# Key idea: MAX(UnitPrice) OVER (PARTITION BY Country) for per-country max;
#           MAX(UnitPrice) OVER () for the global maximum.

user_sql_1 = """
    SELECT
        Country,
        StockCode,
        Description,
        UnitPrice,
        MAX(UnitPrice) OVER (PARTITION BY Country) AS country_max_price,
        MAX(UnitPrice) OVER ()                     AS global_max_price
    FROM retail_data
    WHERE UnitPrice > 0
"""




check_exercise(
    number=1,
    description="Max unit price per country and global maximum on every row",
    user_sql=user_sql_1,
    validation_fn=validate_max_ex1,
    con=con,
    hint="MAX(UnitPrice) OVER (PARTITION BY Country) and MAX(UnitPrice) OVER () for the global maximum",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Using invoice-level revenue, compute the running maximum invoice revenue
# per customer and flag each row as 'new_record' when it equals the running max.
#
# Key idea: aggregate per-invoice revenue first, then
#           MAX(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)
#           tracks the highest value seen up to each row (running maximum).

user_sql_2 = """
    WITH invoice_revenue AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            SUM(Quantity * UnitPrice) AS invoice_revenue
        FROM retail_data
        WHERE CustomerID IS NOT NULL AND Quantity > 0
        GROUP BY CustomerID, InvoiceDate, InvoiceNo
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        invoice_revenue,
        MAX(invoice_revenue) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
        ) AS running_max_revenue,
        CASE
            WHEN invoice_revenue = MAX(invoice_revenue) OVER (
                PARTITION BY CustomerID ORDER BY InvoiceDate
            ) THEN 'new_record'
            ELSE ''
        END AS is_record
    FROM invoice_revenue
"""




check_exercise(
    number=2,
    description="Running maximum invoice revenue per customer with new-record flag",
    user_sql=user_sql_2,
    validation_fn=validate_max_ex2,
    con=con,
    hint="CTE for invoice revenue; MAX(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate); CASE WHEN invoice_revenue = running_max THEN 'new_record' ELSE '' END",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each customer, find their latest purchase date using MAX() OVER() and
# compute days_until_last on every row.
#
# ⚠️  InvoiceDate is a VARCHAR — parse it with STRPTIME before applying MAX().

user_sql_3 = """
    WITH parsed AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS invoice_ts
        FROM retail_data
        WHERE CustomerID IS NOT NULL
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        MAX(invoice_ts) OVER (PARTITION BY CustomerID) AS last_purchase_date,
        DATEDIFF(
            'day',
            invoice_ts,
            MAX(invoice_ts) OVER (PARTITION BY CustomerID)
        ) AS days_until_last
    FROM parsed
"""




check_exercise(
    number=3,
    description="Latest purchase date and days until last purchase per customer",
    user_sql=user_sql_3,
    validation_fn=validate_max_ex3,
    con=con,
    hint=(
        "CTE: STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS invoice_ts; "
        "then MAX(invoice_ts) OVER (PARTITION BY CustomerID) AS last_purchase_date; "
        "DATEDIFF('day', invoice_ts, last_purchase_date) AS days_until_last."
    ),
)
