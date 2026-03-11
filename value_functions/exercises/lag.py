"""
exercises/lag.py — LAG() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/lag.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/lag.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_lag_ex1, validate_lag_ex2, validate_lag_ex3

con = get_connection()

print_header(
    "LAG() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, show the customer's previous purchase Quantity.
# Use LAG() partitioned by CustomerID, ordered by InvoiceDate.
# Rows with no prior purchase should show NULL for prev_quantity.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo, Quantity, prev_quantity

user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: LAG(Quantity, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)
    -- Required columns: CustomerID, InvoiceDate, InvoiceNo, Quantity, prev_quantity
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
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Calculate the revenue delta between consecutive invoices per customer.
# Revenue per invoice = SUM(Quantity * UnitPrice) — only positive quantities.
# Use LAG() to retrieve the previous invoice's revenue, then subtract.
# Use 0 as the default when there is no prior invoice.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo, revenue,
#                   prev_revenue, revenue_delta

user_sql_2 = """
    -- YOUR SQL HERE
    -- Hint: Aggregate revenue in a CTE, then apply LAG(revenue, 1, 0)
    -- OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS prev_revenue
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
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# Identify customers who placed their second purchase in a different country
# compared to their first purchase. Use LAG() on Country (per CustomerID,
# ordered by InvoiceDate). Return only rows where the country changed.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo, Country, prev_country

user_sql_3 = """
    -- YOUR SQL HERE
    -- Hint: DISTINCT per (CustomerID, InvoiceNo, InvoiceDate, Country) first,
    --       then LAG(Country) and filter WHERE Country <> prev_country
"""


check_exercise(
    number=3,
    description="Find customers whose purchase country changed from their previous purchase",
    user_sql=user_sql_3,
    validation_fn=validate_lag_ex3,
    con=con,
    hint="LAG(Country) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS prev_country, then WHERE Country <> prev_country",
)
