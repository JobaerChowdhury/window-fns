"""
exercises/min.py — MIN() OVER() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/min.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/min.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_min_ex1, validate_min_ex2, validate_min_ex3

con = get_connection()

print_header(
    "MIN() OVER() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each row, show the minimum UnitPrice across the entire dataset
# (global_min_price) and the minimum UnitPrice for that row's Country
# (country_min_price). Only include rows where UnitPrice > 0.
# Required columns: Country, StockCode, Description, UnitPrice,
#                   country_min_price, global_min_price

user_sql_1 = """
    -- YOUR SQL HERE
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
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Using invoice-level revenue, compute the running minimum invoice revenue
# per customer ordered by InvoiceDate (cheapest invoice seen so far).
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   invoice_revenue, running_min_revenue
# Only CustomerID IS NOT NULL, Quantity > 0.

user_sql_2 = """
    -- YOUR SQL HERE
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
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For each customer, find their earliest purchase date (first_purchase_date)
# using MIN() OVER() and compute days_since_first on every row.
#
# ⚠️  Warning: InvoiceDate is stored as a VARCHAR string. Applying MIN() on it
# directly gives the WRONG answer (string / lexicographic order).
# Parse it to a timestamp first using STRPTIME.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   first_purchase_date, days_since_first
# Only CustomerID IS NOT NULL.

user_sql_3 = """
    -- YOUR SQL HERE
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
