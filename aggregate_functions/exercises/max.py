"""
exercises/max.py — MAX() OVER() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/max.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/max.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_max_ex1, validate_max_ex2, validate_max_ex3

con = get_connection()

print_header(
    "MAX() OVER() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each row, show the maximum UnitPrice across the entire dataset
# (global_max_price) and the maximum UnitPrice for that row's Country
# (country_max_price). Only include rows where UnitPrice > 0.
# Required columns: Country, StockCode, Description, UnitPrice,
#                   country_max_price, global_max_price

user_sql_1 = """
    -- YOUR SQL HERE
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
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Using invoice-level revenue, compute the running maximum invoice revenue
# per customer ordered by InvoiceDate (biggest invoice seen so far).
# Flag each row as 'new_record' when invoice_revenue equals running_max_revenue.
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   invoice_revenue, running_max_revenue, is_record
# Only CustomerID IS NOT NULL, Quantity > 0.

user_sql_2 = """
    -- YOUR SQL HERE
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
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For each customer, find their latest purchase date (last_purchase_date)
# using MAX() OVER() and compute days_until_last on every row (how many days
# remain until the customer's final recorded purchase).
#
# ⚠️  Warning: InvoiceDate is stored as a VARCHAR string. Applying MAX() on it
# directly gives the WRONG answer (string / lexicographic order).
# Parse it to a timestamp first using STRPTIME.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   last_purchase_date, days_until_last
# Only CustomerID IS NOT NULL.

user_sql_3 = """
    -- YOUR SQL HERE
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
