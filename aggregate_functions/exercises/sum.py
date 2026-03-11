"""
exercises/sum.py — SUM() OVER() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/sum.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/sum.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_sum_ex1, validate_sum_ex2, validate_sum_ex3

con = get_connection()

print_header(
    "SUM() OVER() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, compute the total revenue for the entire dataset
# (grand_total) and the total revenue for the row's country (country_total).
# Include: Country, InvoiceNo, StockCode, line_revenue,
#          country_total, grand_total
# Only include rows where Quantity > 0 and UnitPrice > 0.

user_sql_1 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=1,
    description="Total revenue per country and grand total on every row",
    user_sql=user_sql_1,
    validation_fn=validate_sum_ex1,
    con=con,
    hint="SUM(Quantity * UnitPrice) OVER (PARTITION BY Country) and SUM(Quantity * UnitPrice) OVER () for the grand total",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Using invoice-level revenue (SUM per InvoiceNo), compute a running
# cumulative revenue per customer ordered by InvoiceDate.
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   invoice_revenue, cumulative_revenue
# Only include CustomerID IS NOT NULL and Quantity > 0.

user_sql_2 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=2,
    description="Running cumulative revenue per customer ordered by date",
    user_sql=user_sql_2,
    validation_fn=validate_sum_ex2,
    con=con,
    hint="CTE: aggregate SUM(Quantity*UnitPrice) per invoice; then SUM(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For each customer invoice, compute what percentage of the customer's
# ALL-TIME revenue this single invoice represents.
# Required columns: CustomerID, InvoiceDate, InvoiceNo,
#                   invoice_revenue, customer_total, pct_of_total
# Only CustomerID IS NOT NULL, Quantity > 0.
# Filter out customers whose customer_total = 0 (rounding edge case).
# Round pct_of_total to 1 decimal place.

user_sql_3 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=3,
    description="Each invoice as a percentage of the customer's all-time revenue",
    user_sql=user_sql_3,
    validation_fn=validate_sum_ex3,
    con=con,
    hint=(
        "Two-CTE approach: (1) invoice_totals — SUM(Quantity*UnitPrice) per invoice; "
        "(2) with_totals — add SUM(invoice_revenue) OVER (PARTITION BY CustomerID) as customer_total; "
        "final SELECT: WHERE customer_total > 0, then ROUND(100.0 * invoice_revenue / customer_total, 1) as pct_of_total."
    ),
)
