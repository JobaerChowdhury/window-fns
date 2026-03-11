"""
exercises/last_value.py — LAST_VALUE() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/last_value.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/last_value.py

⚠️  Remember: LAST_VALUE() requires an explicit frame clause:
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_last_value_ex1, validate_last_value_ex2, validate_last_value_ex3

con = get_connection()

print_header(
    "LAST_VALUE() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt. "
    "Don't forget the ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING frame!",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, show the StockCode of the LAST item the customer
# ever purchased (by InvoiceDate). Every row for a customer should carry
# the same last_stockcode value.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo, StockCode,
#                   last_stockcode

user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: LAST_VALUE(StockCode) OVER (
    --           PARTITION BY CustomerID
    --           ORDER BY InvoiceDate
    --           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    --       ) AS last_stockcode
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
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# For each StockCode in each Country, compute avg_price and attach the
# price of the MOST EXPENSIVE StockCode in that Country (priciest_in_country).
# Order by avg_price ASC within the partition so LAST_VALUE picks the maximum.
# Use the full frame clause.
#
# Required columns: Country, StockCode, avg_price, priciest_in_country

user_sql_2 = """
    -- YOUR SQL HERE
    -- Hint: aggregate AVG(UnitPrice) per (Country, StockCode) first,
    --       then LAST_VALUE(avg_price) OVER (PARTITION BY Country ORDER BY avg_price ASC
    --           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS priciest_in_country
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
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For each customer, show both their first and last purchase date on every
# invoice row, plus the total customer lifetime in days
# (last_purchase_day - first_purchase_day).
#
# Required columns: CustomerID, invoice_day, InvoiceNo,
#                   first_purchase_day, last_purchase_day, lifetime_days

user_sql_3 = """
    -- YOUR SQL HERE
    -- Hint: CTE with CAST(STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS DATE),
    --       FIRST_VALUE(invoice_day) OVER (...) AS first_purchase_day,
    --       LAST_VALUE(invoice_day)  OVER (...) AS last_purchase_day,
    --       DATEDIFF('day', first_purchase_day, last_purchase_day) AS lifetime_days
"""


check_exercise(
    number=3,
    description="Customer lifetime in days using FIRST_VALUE and LAST_VALUE together",
    user_sql=user_sql_3,
    validation_fn=validate_last_value_ex3,
    con=con,
    hint="FIRST_VALUE and LAST_VALUE both need ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING; subtract to get lifetime_days",
)
