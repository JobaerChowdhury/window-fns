"""
solutions/min.py — MIN() OVER() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the MIN() OVER() exercises.
Refer to this file ONLY if you are stuck on exercises/min.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_min_ex1, validate_min_ex2, validate_min_ex3

con = get_connection()

print_header(
    "MIN() OVER() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each row, show the minimum UnitPrice globally and per Country.
#
# Key idea: MIN(UnitPrice) OVER (PARTITION BY Country) for per-country min;
#           MIN(UnitPrice) OVER () for the global minimum.

user_sql_1 = """
    SELECT
        Country,
        StockCode,
        Description,
        UnitPrice,
        MIN(UnitPrice) OVER (PARTITION BY Country) AS country_min_price,
        MIN(UnitPrice) OVER ()                     AS global_min_price
    FROM retail_data
    WHERE UnitPrice > 0
"""




check_exercise(
    number=1,
    description="Min unit price per country and global minimum on every row",
    user_sql=user_sql_1,
    validation_fn=validate_min_ex1,
    con=con,
    hint="MIN(UnitPrice) OVER (PARTITION BY Country) and MIN(UnitPrice) OVER () for the global minimum",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Using invoice-level revenue, compute the running minimum invoice revenue
# per customer ordered by InvoiceDate (cheapest invoice seen so far).
#
# Key idea: aggregate per-invoice revenue first, then
#           MIN(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)
#           tracks the lowest value seen up to each row (running minimum).

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
        MIN(invoice_revenue) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
        ) AS running_min_revenue
    FROM invoice_revenue
"""




check_exercise(
    number=2,
    description="Running minimum invoice revenue per customer",
    user_sql=user_sql_2,
    validation_fn=validate_min_ex2,
    con=con,
    hint="CTE for invoice revenue; MIN(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each customer, find their earliest purchase date using MIN() OVER()
# and compute days_since_first on every row.
#
# ⚠️  InvoiceDate is a VARCHAR — parse it with STRPTIME before applying MIN().

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
        MIN(invoice_ts) OVER (PARTITION BY CustomerID) AS first_purchase_date,
        DATEDIFF(
            'day',
            MIN(invoice_ts) OVER (PARTITION BY CustomerID),
            invoice_ts
        ) AS days_since_first
    FROM parsed
"""




check_exercise(
    number=3,
    description="Earliest purchase date and days since first purchase per customer",
    user_sql=user_sql_3,
    validation_fn=validate_min_ex3,
    con=con,
    hint=(
        "CTE: STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS invoice_ts; "
        "then MIN(invoice_ts) OVER (PARTITION BY CustomerID) AS first_purchase_date; "
        "DATEDIFF('day', first_purchase_date, invoice_ts) AS days_since_first."
    ),
)
