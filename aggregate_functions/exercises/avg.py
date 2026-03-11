"""
exercises/avg.py — AVG() OVER() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/avg.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/avg.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_avg_ex1, validate_avg_ex2, validate_avg_ex3

con = get_connection()

print_header(
    "AVG() OVER() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each StockCode, compute the average UnitPrice across the whole dataset
# (global_avg_price) and per Country (country_avg_price).
# Show rows where UnitPrice > 0.
# Required columns: Country, StockCode, UnitPrice,
#                   country_avg_price, global_avg_price

user_sql_1 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=1,
    description="Average unit price per country and global average on every row",
    user_sql=user_sql_1,
    validation_fn=validate_avg_ex1,
    con=con,
    hint="AVG(UnitPrice) OVER (PARTITION BY Country) and AVG(UnitPrice) OVER () for the global average",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Using invoice-level revenue (aggregate Quantity*UnitPrice per invoice),
# compute the running average invoice value per customer ordered by InvoiceDate.
# Flag each row as 'above_avg' or 'below_avg' relative to the running average.
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   invoice_revenue, running_avg, spend_trend
# Only CustomerID IS NOT NULL, Quantity > 0.

user_sql_2 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=2,
    description="Running average invoice spend per customer with above/below flag",
    user_sql=user_sql_2,
    validation_fn=validate_avg_ex2,
    con=con,
    hint="CTE for invoice revenue; AVG(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate); CASE WHEN invoice_revenue > running_avg THEN 'above_avg' ELSE 'below_avg' END",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For each customer, compute a 3-invoice moving average of invoice revenue
# (ordered by InvoiceDate) and compare it to the customer's all-time average.
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   invoice_revenue, avg_all_time, moving_avg_3
# Only CustomerID IS NOT NULL, Quantity > 0.

user_sql_3 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=3,
    description="3-invoice moving average vs all-time average per customer",
    user_sql=user_sql_3,
    validation_fn=validate_avg_ex3,
    con=con,
    hint="AVG(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3",
)
