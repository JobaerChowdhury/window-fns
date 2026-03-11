"""
solutions/lag.py — LAG() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the LAG() exercises.
Refer to this file ONLY if you are stuck on exercises/lag.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_lag_ex1, validate_lag_ex2, validate_lag_ex3

con = get_connection()

print_header(
    "LAG() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, show the customer's previous purchase Quantity.
#
# Key idea: LAG(Quantity, 1) looks back 1 row within the customer's window.
#           The first row per customer has no prior row → NULL.

user_sql_1 = """
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        Quantity,
        LAG(Quantity, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS prev_quantity
    FROM retail_data
"""


check_exercise(
    number=1,
    description="Show previous purchase Quantity for each customer",
    user_sql=user_sql_1,
    validation_fn=validate_lag_ex1,
    con=con,
    hint="LAG(Quantity, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS prev_quantity",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Calculate the revenue delta between consecutive invoices per customer.
#
# Key idea: aggregate per-invoice revenue in a CTE, then LAG(revenue, 1, 0)
#           retrieves the previous invoice's revenue (0 when there is none).
#           revenue_delta = revenue - prev_revenue.

user_sql_2 = """
    WITH invoice_revenue AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            SUM(Quantity * UnitPrice) AS revenue
        FROM retail_data
        WHERE Quantity > 0 AND CustomerID IS NOT NULL
        GROUP BY CustomerID, InvoiceDate, InvoiceNo
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        revenue,
        LAG(revenue, 1, 0) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS prev_revenue,
        revenue - LAG(revenue, 1, 0) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS revenue_delta
    FROM invoice_revenue
"""


check_exercise(
    number=2,
    description="Revenue delta between consecutive customer invoices",
    user_sql=user_sql_2,
    validation_fn=validate_lag_ex2,
    con=con,
    hint="CTE with SUM(Quantity*UnitPrice) per invoice, then LAG(revenue, 1, 0) and revenue - prev_revenue",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Identify customers who placed a purchase in a different country compared
# to their previous purchase.
#
# Key idea: deduplicate to one row per (CustomerID, InvoiceNo, InvoiceDate, Country)
#           first, then LAG(Country) to get prev_country, finally filter
#           WHERE Country <> prev_country (excludes NULL first-purchase rows).

user_sql_3 = """
    WITH distinct_invoices AS (
        SELECT DISTINCT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            Country
        FROM retail_data
        WHERE CustomerID IS NOT NULL
    ), with_prev AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            Country,
            LAG(Country) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS prev_country
        FROM distinct_invoices
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        Country,
        prev_country
    FROM with_prev
    WHERE Country <> prev_country
"""


check_exercise(
    number=3,
    description="Find customers whose purchase country changed from their previous purchase",
    user_sql=user_sql_3,
    validation_fn=validate_lag_ex3,
    con=con,
    hint="LAG(Country) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS prev_country, then WHERE Country <> prev_country",
)
